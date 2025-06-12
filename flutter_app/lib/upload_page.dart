import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:file_picker/file_picker.dart';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  _UploadPageState createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  String firstName = '';
  int userId = -1;
  List documents = [];

  @override
  void initState() {
    super.initState();
    loadUserDetails();
  }

  Future<void> loadUserDetails() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');
    if (token == null) {
      Navigator.pushReplacementNamed(context, '/login');
      return;
    }

    // Decode JWT payload
    final parts = token.split('.');
    final payload = json.decode(utf8.decode(base64Url.decode(base64Url.normalize(parts[1]))));

    setState(() {
      userId = payload['user_id'];
      firstName = payload['first_name'] ?? ''; // You can attach `first_name` during login if needed
    });

    fetchDocuments();
  }

  Future<void> fetchDocuments() async {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/api/documents/$userId/'),
    );

    if (response.statusCode == 200) {
      setState(() {
        documents = json.decode(response.body);
      });
    }
  }

  Future<void> uploadFile() async {
    final result = await FilePicker.platform.pickFiles();
    if (result == null || result.files.isEmpty) return;

    final fileBytes = result.files.first.bytes;
    final fileName = result.files.first.name;

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://127.0.0.1:8000/api/upload/'),
    );

    request.fields['user_id'] = userId.toString();
    request.files.add(http.MultipartFile.fromBytes('file', fileBytes!, filename: fileName));

    final response = await request.send();

    if (response.statusCode == 200) {
      fetchDocuments();
    } else {
      print('Upload failed');
    }
  }

  Future<void> verifyDocument(int docId) async {
    final res = await http.post(Uri.parse('http://127.0.0.1:8000/api/verify/$docId/'));
    if (res.statusCode == 200) fetchDocuments();
  }

  Future<void> deleteDocument(int docId) async {
    final res = await http.delete(Uri.parse('http://127.0.0.1:8000/api/delete/$docId/'));
    if (res.statusCode == 200) fetchDocuments();
  }

  Future<void> logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('jwt_token');
    Navigator.pushReplacementNamed(context, '/login');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text('Hello, $firstName')),
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () => logout(context),
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ElevatedButton.icon(
              onPressed: uploadFile,
              icon: Icon(Icons.upload_file),
              label: Text("Choose or Drag File"),
            ),
            SizedBox(height: 20),
            Expanded(
              child: documents.isEmpty
                  ? Text('No documents uploaded.')
                  : ListView.builder(
                      itemCount: documents.length,
                      itemBuilder: (context, index) {
                        final doc = documents[index];
                        return Card(
                          child: ListTile(
                            title: Text(doc['filename']),
                            subtitle: Text('Verdict: ${doc['verdict']}, Score: ${doc['fraud_score']}'),
                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                IconButton(
                                  icon: Icon(Icons.verified),
                                  tooltip: 'Verify',
                                  onPressed: () => verifyDocument(doc['id']),
                                ),
                                IconButton(
                                  icon: Icon(Icons.delete),
                                  tooltip: 'Delete',
                                  onPressed: () => deleteDocument(doc['id']),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

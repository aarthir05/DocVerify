import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  String username = '', password = '';
  bool isLoading = false;
  String error = '';

  Future<void> login() async {
  if (!_formKey.currentState!.validate()) return;
  setState(() {
    isLoading = true;
    error = '';
  });

  final response = await http.post(
    Uri.parse('http://127.0.0.1:8000/api/token/'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode({'username': username, 'password': password}),
  );

  setState(() => isLoading = false);

  if (response.statusCode == 200) {
    final token = json.decode(response.body)['access'];
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt_token', token);
    Navigator.pushReplacementNamed(context, '/upload');
  } else {
    setState(() => error = 'Invalid credentials');
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.all(20),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  Text('Login', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
                  SizedBox(height: 20),
                  TextFormField(
                    decoration: InputDecoration(labelText: 'Username'),
                    onChanged: (val) => username = val,
                    validator: (val) => val!.isEmpty ? 'Enter username' : null,
                  ),
                  SizedBox(height: 16),
                  TextFormField(
                    obscureText: true,
                    decoration: InputDecoration(labelText: 'Password'),
                    onChanged: (val) => password = val,
                    validator: (val) => val!.isEmpty ? 'Enter password' : null,
                  ),
                  SizedBox(height: 20),
                  if (error.isNotEmpty)
                    Text(error, style: TextStyle(color: Colors.red)),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: isLoading ? null : login,
                    child: isLoading ? CircularProgressIndicator() : Text('Login'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, '/signup');
                    },
                    child: Text('Don\'t have an account? Sign up'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

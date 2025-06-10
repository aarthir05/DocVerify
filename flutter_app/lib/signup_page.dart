import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignupPage extends StatefulWidget {
  @override
  _SignupPageState createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final _formKey = GlobalKey<FormState>();
  String firstName = '', lastName = '', email = '', username = '', password = '', confirmPassword = '';
  String error = '';
  bool isLoading = false;

  Future<void> signup() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      isLoading = true;
      error = '';
    });

    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/signup/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'first_name': firstName,
        'last_name': lastName,
        'email': email,
        'username': username,
        'password': password,
      }),
    );

    setState(() => isLoading = false);

    if (response.statusCode == 200) {
      Navigator.pushReplacementNamed(context, '/login');
    } else {
      final res = json.decode(response.body);
      setState(() => error = res['error'] ?? 'Signup failed');
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
                  Text('Sign Up', style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
                  SizedBox(height: 20),
                  TextFormField(
                    decoration: InputDecoration(labelText: 'First Name'),
                    onChanged: (val) => firstName = val,
                    validator: (val) => val!.isEmpty ? 'Enter first name' : null,
                  ),
                  SizedBox(height: 10),
                  TextFormField(
                    decoration: InputDecoration(labelText: 'Last Name'),
                    onChanged: (val) => lastName = val,
                  ),
                  SizedBox(height: 10),
                  TextFormField(
                    decoration: InputDecoration(labelText: 'Email'),
                    onChanged: (val) => email = val,
                    validator: (val) => val!.contains('@') ? null : 'Enter valid email',
                  ),
                  SizedBox(height: 10),
                  TextFormField(
                    decoration: InputDecoration(labelText: 'Username'),
                    onChanged: (val) => username = val,
                    validator: (val) => val!.isEmpty ? 'Enter username' : null,
                  ),
                  SizedBox(height: 10),
                  TextFormField(
                    obscureText: true,
                    decoration: InputDecoration(labelText: 'Password'),
                    onChanged: (val) => password = val,
                    validator: (val) => val!.length < 6 ? 'Password too short' : null,
                  ),
                  SizedBox(height: 10),
                  TextFormField(
                    obscureText: true,
                    decoration: InputDecoration(labelText: 'Confirm Password'),
                    onChanged: (val) => confirmPassword = val,
                    validator: (val) =>
                        val != password ? 'Passwords do not match' : null,
                  ),
                  SizedBox(height: 20),
                  if (error.isNotEmpty)
                    Text(error, style: TextStyle(color: Colors.red)),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: isLoading ? null : signup,
                    child: isLoading ? CircularProgressIndicator() : Text('Sign Up'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, '/login');
                    },
                    child: Text('Already have an account? Log in'),
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

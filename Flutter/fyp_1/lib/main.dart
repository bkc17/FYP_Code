import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:fyp_1/read_examples.dart';
import 'firebase_options.dart';
import 'dart:math';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // await Firebase.initializeApp(
  //   options: DefaultFirebaseOptions.currentPlatform,
  // );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final Future<FirebaseApp> _fbapp = Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // home: const MyHomePage(title: 'Flutter Demo Home Page'),
      home: FutureBuilder(
        future: _fbapp,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            print('Snapshot has error! ${snapshot.error.toString()}');
            return const Text('Something went wrong!');
          } else if (snapshot.hasData) {
            return const MyHomePage(title: 'My Amazing Counter App!');
          } else {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
        },
      ),
    );
  }
}

class MyHomePage extends StatelessWidget {
  final String title;
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: [
            const Text('Check out our examples'),
            SizedBox(
              height: 6,
              width: MediaQuery.of(context).size.width,
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ReadExamples(),
                  ),
                );
              },
              child: const Text('Read Examples'),
            ),
            // ElevatedButton(
            //   onPressed: () {},
            //   child: const Text('Write Examples'),
            // ),
          ],
        ),
      ),
    );
  }
}

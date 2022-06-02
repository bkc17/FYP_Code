import 'dart:convert';

import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';

class ReadExamples extends StatefulWidget {
  const ReadExamples({Key? key}) : super(key: key);

  @override
  State<ReadExamples> createState() => _ReadExamplesState();
}

class _ReadExamplesState extends State<ReadExamples> {
  String _displayText = 'Results go here!';
  final _database = FirebaseDatabase.instance.ref('/data_current');
  var decoded_data;
  @override
  void initState() {
    super.initState();
    _activateListeners();
  }

  void _activateListeners() {
    Stream<DatabaseEvent> stream = _database.onValue;
    stream.listen((DatabaseEvent event) {
      // print('Event Type: ${event.type}'); // DatabaseEventType.value;
      // print('Snapshot: ${event.snapshot.value.runtimeType}'); // DataSnapshot
      decoded_data = jsonDecode(jsonEncode(event.snapshot.value));
      setState(() {
        // _displayText = event.snapshot.value.toString();
        // print(decoded_data['temp'].runtimeType);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Read Examples'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.only(top: 15.0),
          child: Column(
            children: [Text(_displayText)],
          ),
        ),
      ),
    );
  }
}

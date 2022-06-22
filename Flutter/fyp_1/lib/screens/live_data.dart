import 'dart:convert';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:fyp_1/constants.dart';
import 'package:fyp_1/components/reusable_card_widget.dart';
import 'live_plot.dart';

class ReadData extends StatefulWidget {
  const ReadData({Key? key}) : super(key: key);
  @override
  State<ReadData> createState() => _ReadDataState();
}

class _ReadDataState extends State<ReadData> {
  final _database = FirebaseDatabase.instance.ref('/Current data');
  var decoded_data;
  String vdd = '0';
  String temp = '0';
  String rot_speed = '0';
  String grad = '0';
  String wind_speed = '0';

  @override
  void initState() {
    super.initState();
    _activateListeners();
  }

  void _activateListeners() {
    Stream<DatabaseEvent> stream = _database.onValue;
    stream.listen((DatabaseEvent event) {
      decoded_data = jsonDecode(jsonEncode(event.snapshot.value));
      setState(() {
        vdd = decoded_data['vdd'].toString();
        temp = decoded_data['temp'].toString();
        rot_speed = decoded_data['rot_speed'].toString();
        grad = decoded_data['grad'].toString();
        wind_speed = decoded_data['wind_speed'].toString();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: kActiveCardColour,
        title: const Text('Live Data'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              ReusableCardWidget(
                title: 'VDD (Volts)',
                data: vdd,
                function: const LivePlot(
                  data: 'vdd',
                  title: 'VDD (Volts)',
                ),
              ), //vdd
              ReusableCardWidget(
                title: 'Temperature (\u00B0C)',
                data: temp,
                function: const LivePlot(
                  data: 'temp',
                  title: 'Temperature (\u00B0C)',
                ),
              ), //temperature
              ReusableCardWidget(
                title: 'Speed (rads/sec)',
                data: rot_speed,
                function: const LivePlot(
                  data: 'rot_speed',
                  title: 'Speed (rads/sec)',
                ),
              ), //rotation speed
              ReusableCardWidget(
                title: 'Gradient (rads/s\u00B2)',
                data: grad,
                function: const LivePlot(
                  data: 'grad',
                  title: 'Gradient (rads/s\u00B2)',
                ),
              ), //gradient
              ReusableCardWidget(
                title: 'Wind Speed (m/s)',
                data: wind_speed,
                function: const LivePlot(
                  data: 'wind_speed',
                  title: 'Wind Speed (m/s)',
                ),
              ), //wind speed
            ],
          ),
        ),
      ),
    );
  }
}

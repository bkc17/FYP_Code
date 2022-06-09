import 'package:flutter/material.dart';
import 'dart:async';
import 'package:firebase_database/firebase_database.dart';
import 'dart:convert';
import '../constants.dart';
import '../components/chart_widget.dart';

class LivePlot extends StatefulWidget {
  final String data;
  final String title;

  const LivePlot({required this.data, required this.title});

  @override
  State<LivePlot> createState() => _LivePlotState();
}

class _LivePlotState extends State<LivePlot> {
  final _database = FirebaseDatabase.instance.ref('/data_current');
  var decoded_data;
  int data_val = 0;
  int counter = 0;
  List<TurbineData> _chartData = <TurbineData>[];

  @override
  void initState() {
    super.initState();
    _chartData = getChartData();
    _activateListeners();
  }

  void _activateListeners() {
    Stream<DatabaseEvent> stream = _database.onValue;
    stream.listen((DatabaseEvent event) {
      decoded_data = jsonDecode(jsonEncode(event.snapshot.value));
      setState(() {
        data_val = decoded_data[widget.data];
        _chartData.add(TurbineData(counter, data_val));
        counter++;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: kActiveCardColour,
        title: const Text('Live Plot'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const SizedBox(
              height: 100,
            ),
            Text(
              widget.title,
              style: kPlotLabelTextStyle,
            ),
            const SizedBox(
              height: 50,
            ),
            Expanded(
              child: chartWidget(chartData: _chartData, counter: counter),
            ),
            const SizedBox(
              height: 150,
            ),
          ],
        ),
      ),
    );
  }

  List<TurbineData> getChartData() {
    final List<TurbineData> chartData = [
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
      TurbineData(0, 0),
    ];
    return chartData;
  }
}

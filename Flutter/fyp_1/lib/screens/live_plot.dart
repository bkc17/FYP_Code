import 'package:flutter/material.dart';
import 'dart:async';
import 'package:firebase_database/firebase_database.dart';
import 'dart:convert';
import '../constants.dart';
import '../components/chart_widget.dart';

class LivePlot extends StatefulWidget {
  @override
  State<LivePlot> createState() => _LivePlotState();
}

class _LivePlotState extends State<LivePlot> {
  final _database = FirebaseDatabase.instance.ref('/data_current');
  var decoded_data;
  int rot_speed = 0;
  int grad = 0;
  int counter = 0;
  List<TurbineData> _chartDataSpeed = <TurbineData>[];
  List<TurbineData> _chartDataGrad = <TurbineData>[];

  @override
  void initState() {
    super.initState();
    _chartDataSpeed = getChartData();
    _chartDataGrad = getChartData();
    _activateListeners();
  }

  void _activateListeners() {
    Stream<DatabaseEvent> stream = _database.onValue;
    stream.listen((DatabaseEvent event) {
      decoded_data = jsonDecode(jsonEncode(event.snapshot.value));
      setState(() {
        // print(decoded_data);
        // vdd = decoded_data['vdd'];
        // temp = decoded_data['temp'];
        rot_speed = decoded_data['rot_speed'];
        grad = decoded_data['grad'];
        _chartDataSpeed.add(TurbineData(counter, rot_speed));
        _chartDataGrad.add(TurbineData(counter, grad));
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
            Expanded(
              //   child: SfCartesianChart(
              //     series: <ChartSeries>[
              //       LineSeries<TurbineData, int>(
              //           dataSource: _chartDataSpeed,
              //           xValueMapper: (TurbineData speed, _) => speed.x,
              //           yValueMapper: (TurbineData speed, _) => speed.speed),
              //     ],
              //     // primaryXAxis: DateTimeAxis(),
              //
              //     primaryXAxis: NumericAxis(
              //       visibleMinimum:
              //           _chartDataSpeed[_chartDataSpeed.length - 5].x.toDouble(),
              //       visibleMaximum: counter + 2,
              //     ),
              //     primaryYAxis: NumericAxis(),
              //     zoomPanBehavior: ZoomPanBehavior(
              //       enablePanning: true,
              //     ),
              //   ),
              child: chartWidget(chartData: _chartDataSpeed, counter: counter),
            ),
            Expanded(
              child: chartWidget(chartData: _chartDataGrad, counter: counter),
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

import 'package:flutter/material.dart';
import 'package:fyp_1/constants.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class chartWidget extends StatelessWidget {
  const chartWidget({
    Key? key,
    required List<TurbineData> chartData,
    required this.counter,
  })  : _chartData = chartData,
        super(key: key);

  final List<TurbineData> _chartData;
  final int counter;

  @override
  Widget build(BuildContext context) {
    return SfCartesianChart(
      series: <ChartSeries>[
        LineSeries<TurbineData, int>(
            dataSource: _chartData,
            pointColorMapper: (TurbineData data, _) => kAccentColor,
            markerSettings: const MarkerSettings(isVisible: true),
            dataLabelSettings: const DataLabelSettings(
              isVisible: true,
              opacity: 0.4,
              textStyle: TextStyle(fontSize: 12),
            ),
            xValueMapper: (TurbineData speed, _) => speed.x,
            yValueMapper: (TurbineData speed, _) => speed.speed),
      ],
      // primaryXAxis: DateTimeAxis(),
      primaryXAxis: NumericAxis(
          visibleMinimum: _chartData[_chartData.length - 5].x.toDouble(),
          visibleMaximum: counter + 2,
          labelStyle: const TextStyle(fontSize: 15),
          majorGridLines: const MajorGridLines(width: 2),
          decimalPlaces: 0),
      primaryYAxis: NumericAxis(
        labelStyle: const TextStyle(fontSize: 15),
        decimalPlaces: 1,
        majorGridLines: const MajorGridLines(width: 2),
      ),
      zoomPanBehavior: ZoomPanBehavior(
        enablePanning: true,
      ),
    );
  }
}

class TurbineData {
  TurbineData(this.x, this.speed);
  final int x;
  final int speed;
}

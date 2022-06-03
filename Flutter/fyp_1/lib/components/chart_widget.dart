import 'package:flutter/material.dart';
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
            xValueMapper: (TurbineData speed, _) => speed.x,
            yValueMapper: (TurbineData speed, _) => speed.speed),
      ],
      // primaryXAxis: DateTimeAxis(),

      primaryXAxis: NumericAxis(
        visibleMinimum: _chartData[_chartData.length - 5].x.toDouble(),
        visibleMaximum: counter + 2,
      ),
      primaryYAxis: NumericAxis(),
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

import 'package:flutter/material.dart';
import '../screens/live_plot.dart';

class ReusableCardBackground extends StatelessWidget {
  ReusableCardBackground({
    required this.colour,
    required this.cardChild,
    required this.function,
  });

  final Color colour;
  final Widget cardChild;
  final LivePlot function;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Container(
        margin: const EdgeInsets.only(
            top: 10.0, bottom: 10.0, left: 50.0, right: 50.0),
        padding: const EdgeInsets.all(25.0),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10.0),
          color: colour,
        ),
        child: cardChild,
      ),
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => function,
          ),
        );
      },
    );
  }
}

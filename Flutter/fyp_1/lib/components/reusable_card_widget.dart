import 'package:flutter/material.dart';
import 'package:fyp_1/screens/live_plot.dart';
import '../constants.dart';
import 'reusable_card_background.dart';

class ReusableCardWidget extends StatelessWidget {
  const ReusableCardWidget({
    Key? key,
    required this.title,
    required this.data,
    required this.function,
  }) : super(key: key);

  final String title;
  final String data;
  final LivePlot function;

  @override
  Widget build(BuildContext context) {
    return ReusableCardBackground(
      colour: kActiveCardColour,
      cardChild: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Text(
            title,
            style: kLabelTextStyle,
          ),
          const SizedBox(
            height: 20,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                data,
                style: kNumberTextStyle,
              ),
              const SizedBox(
                width: 5,
              ),
            ],
          ),
        ],
      ),
      function: function,
    );
  }
}

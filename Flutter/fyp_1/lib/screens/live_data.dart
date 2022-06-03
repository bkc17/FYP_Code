import 'dart:convert';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:fyp_1/constants.dart';
import 'package:fyp_1/components/reusable_card.dart';

class ReadData extends StatefulWidget {
  const ReadData({Key? key}) : super(key: key);

  @override
  State<ReadData> createState() => _ReadDataState();
}

class _ReadDataState extends State<ReadData> {
  final _database = FirebaseDatabase.instance.ref('/data_current');
  var decoded_data;
  String vdd = '0';
  String temp = '0';
  String rot_speed = '0';
  String grad = '0';
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
      // body: Center(
      //   child: Padding(
      //     padding: const EdgeInsets.all(20.0),
      //     child: Column(
      //       // crossAxisAlignment: CrossAxisAlignment.stretch,
      //       mainAxisAlignment: MainAxisAlignment.center,
      //       children: [
      //         Row(
      //           children: [
      //             Expanded(
      //               child: ReusableCard(
      //                 colour: kActiveCardColour,
      //                 cardChild: Column(
      //                   mainAxisAlignment: MainAxisAlignment.center,
      //                   children: <Widget>[
      //                     const Text(
      //                       'VDD',
      //                       style: kLabelTextStyle,
      //                     ),
      //                     Text(
      //                       '${decoded_data["vdd"]}',
      //                       style: kNumberTextStyle,
      //                     ),
      //                   ],
      //                 ),
      //               ),
      //             ),
      //             Expanded(
      //               child: ReusableCard(
      //                 colour: kActiveCardColour,
      //                 cardChild: Column(
      //                   mainAxisAlignment: MainAxisAlignment.center,
      //                   children: <Widget>[
      //                     const Text(
      //                       'Temperature',
      //                       style: kLabelTextStyle,
      //                     ),
      //                     Text(
      //                       '${decoded_data["temp"]}',
      //                       style: kNumberTextStyle,
      //                     ),
      //                   ],
      //                 ),
      //               ),
      //             ),
      //           ],
      //         ),
      //         const SizedBox(
      //           height: 30,
      //         ),
      //         Row(
      //           children: [
      //             Expanded(
      //               child: ReusableCard(
      //                 colour: kActiveCardColour,
      //                 cardChild: Column(
      //                   mainAxisAlignment: MainAxisAlignment.center,
      //                   children: <Widget>[
      //                     const Text(
      //                       'Rotation Speed',
      //                       style: kLabelTextStyle,
      //                     ),
      //                     Text(
      //                       '${decoded_data["rot_speed"]}',
      //                       style: kNumberTextStyle,
      //                     ),
      //                   ],
      //                 ),
      //               ),
      //             ),
      //             Expanded(
      //               child: ReusableCard(
      //                 colour: kActiveCardColour,
      //                 cardChild: Column(
      //                   mainAxisAlignment: MainAxisAlignment.center,
      //                   children: <Widget>[
      //                     const Text(
      //                       'Gradient',
      //                       style: kLabelTextStyle,
      //                     ),
      //                     Text(
      //                       '${decoded_data["grad"]}',
      //                       style: kNumberTextStyle,
      //                     ),
      //                   ],
      //                 ),
      //               ),
      //             ),
      //           ],
      //         ),
      //       ],
      //     ),
      //   ),
      // ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ReusableCard(
              colour: kActiveCardColour,
              cardChild: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text(
                    'VDD (Volts)',
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
                        vdd,
                        style: kNumberTextStyle,
                      ),
                      const SizedBox(
                        width: 5,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            ReusableCard(
              colour: kActiveCardColour,
              cardChild: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text(
                    'Temperature (\u00B0C)',
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
                        temp,
                        style: kNumberTextStyle,
                      ),
                      const SizedBox(
                        width: 5,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            ReusableCard(
              colour: kActiveCardColour,
              cardChild: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text(
                    'Speed (rads/sec)',
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
                        rot_speed,
                        style: kNumberTextStyle,
                      ),
                      const SizedBox(
                        width: 5,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            ReusableCard(
              colour: kActiveCardColour,
              cardChild: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text(
                    'Gradient (rads/s\u00B2)',
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
                        grad,
                        style: kNumberTextStyle,
                      ),
                      const SizedBox(
                        width: 5,
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

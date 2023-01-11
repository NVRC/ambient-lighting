import { ActivityIndicator, StyleSheet } from 'react-native';

import { View, Text } from 'controller/components/Themed';
import { RootTabScreenProps } from '../../types';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';
import { SketchPicker, ColorChangeHandler } from 'react-color';
import { Led, usePostStripLedsStripsStripIdLedsPostMutation, useReadStripStripsStripIdGetQuery } from 'controller/redux/services/ledStripsApi';

const STRIP_ID = 1;

interface LedMap {
    [key: string]: Led
}

export default function QuickSetTabScreen({ navigation }: RootTabScreenProps<'QuickSetTab'>) {
  const { colorScheme } = useAppSelector(getSettings)

  const { data: strip, isLoading, isFetching, isError } = useReadStripStripsStripIdGetQuery({
    stripId: 1
  });
  const [postStripLeds] = usePostStripLedsStripsStripIdLedsPostMutation();


  if (isLoading || isFetching || isError || strip === undefined){
    return (
        <View colorScheme={colorScheme} style={styles.container}>
            <ActivityIndicator />
        </View>
    )
  }

  const onChangeComplete: ColorChangeHandler = (color) => {
    const rgb = {
        red: color.rgb.r,
        green: color.rgb.g,
        blue: color.rgb.b,
    }
    const ledMap: LedMap = {};
    Object.entries(strip?.leds).forEach((tuple) => {
        const [ index, led ] = tuple;
        const newLed = {
            ...led,
            color: rgb,
        }
        ledMap[index] = newLed;
    })
    postStripLeds({
        stripId: STRIP_ID,
        body: ledMap
    })
  }
  return (
    <View colorScheme={colorScheme} style={styles.container}>
        <SketchPicker onChangeComplete={onChangeComplete}/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});

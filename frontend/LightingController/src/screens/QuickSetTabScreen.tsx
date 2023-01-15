import { ActivityIndicator, StyleSheet } from 'react-native';

import { View } from 'controller/components/Themed';
import { RootTabScreenProps } from '../../types';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';
import { RgbColor, RgbColorPicker } from 'react-colorful';
import { Led } from 'controller/redux/services/auto_gen/ledStripsApi'
import { usePostStripLedsStripsStripIdLedsPostMutation, useReadStripStripsStripIdGetQuery } from 'controller/redux/services/ledStripsApi';

import { STRIP_ID } from 'controller/redux/store'
interface LedMap {
    [key: string]: Led
}

export default function QuickSetTabScreen({ navigation }: RootTabScreenProps<'QuickSetTab'>) {
  const { colorScheme } = useAppSelector(getSettings)

  const { data: strip, isLoading, isFetching, isError } = useReadStripStripsStripIdGetQuery({
    stripId: STRIP_ID,
  });
  const [postStripLeds] = usePostStripLedsStripsStripIdLedsPostMutation();


  if (isLoading || isFetching || isError || strip === undefined){
    return (
        <View colorScheme={colorScheme} style={styles.container}>
            <ActivityIndicator />
        </View>
    )
  }

  const onChangeComplete = (color: RgbColor) => {
    const rgb = {
        red: color.r,
        green: color.g,
        blue: color.b,
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
        <RgbColorPicker onChange={onChangeComplete}/>
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

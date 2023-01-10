import { StyleSheet } from 'react-native';

import EditScreenInfo from 'controller/components/EditScreenInfo';
import { Text, View } from 'controller/components/Themed';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

export default function SettingsTabScreen() {
  const { colorScheme } = useAppSelector(getSettings);
  return (
    <View colorScheme={colorScheme} style={styles.container}>
      <Text colorScheme={colorScheme} style={styles.title}>Tab Two</Text>
      <View  colorScheme={colorScheme} style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="/screens/SettingsTabScreen.tsx" />
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

import { StatusBar } from 'expo-status-bar';
import { Platform, StyleSheet } from 'react-native';

import EditScreenInfo from 'controller/components/EditScreenInfo';
import { Text, View } from 'controller/components/Themed';

import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

export default function ModalScreen() {
  const { colorScheme } = useAppSelector(getSettings)

  return (
    <View colorScheme={colorScheme} style={styles.container}>
      <Text colorScheme={colorScheme} style={styles.title}>Modal</Text>
      <View colorScheme={colorScheme} style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="/screens/ModalScreen.tsx" />

      {/* Use a light status bar on iOS to account for the black space above the modal */}
      <StatusBar style={Platform.OS === 'ios' ? 'light' : 'auto'} />
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

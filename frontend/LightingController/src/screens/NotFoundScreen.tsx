import { StyleSheet, TouchableOpacity } from 'react-native';

import { Text, View } from 'controller/components/Themed';
import { RootStackScreenProps } from '../../types';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

export default function NotFoundScreen({ navigation }: RootStackScreenProps<'NotFound'>) {
  const { colorScheme } = useAppSelector(getSettings)
  return (
    <View colorScheme={colorScheme} style={styles.container}>
      <Text colorScheme={colorScheme} style={styles.title}>This screen doesn't exist.</Text>
      <TouchableOpacity onPress={() => navigation.replace('Root')} style={styles.link}>
        <Text colorScheme={colorScheme} style={styles.linkText}>Go to home screen!</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
  linkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});

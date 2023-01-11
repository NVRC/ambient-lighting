import { StatusBar } from 'expo-status-bar';
import { Platform, StyleSheet, TextInput, ActivityIndicator, TextInputChangeEventData, NativeSyntheticEvent } from 'react-native';

import EditScreenInfo from 'controller/components/EditScreenInfo';
import { Text, View } from 'controller/components/Themed';

import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';
import { STRIP_ID } from 'controller/redux/store';

import { Strip, usePostStripStripsStripIdPostMutation, useReadStripStripsStripIdGetQuery } from 'controller/redux/services/ledStripsApi';

import { useForm, SubmitHandler } from 'react-hook-form';

export default function ModalScreen() {
  const { colorScheme } = useAppSelector(getSettings)

  const { data: strip, isLoading, isFetching, isError } = useReadStripStripsStripIdGetQuery({
    stripId: STRIP_ID
  });

  const [postStrip] = usePostStripStripsStripIdPostMutation();

  const { handleSubmit, register } = useForm<Strip>({
    defaultValues: strip
  });

  if (isLoading || isFetching || isError || strip === undefined){
    return (
        <View colorScheme={colorScheme} style={styles.container}>
            <ActivityIndicator />
        </View>
    )
  }


  const onSubmit = (data: Strip) => {
    postStrip({
        stripId: STRIP_ID,
        strip: {
            ...strip,
            brightness: data.brightness,
        }
    })
  }


  return (
    <View colorScheme={colorScheme} style={styles.container}>
      <form onSubmit={handleSubmit(onSubmit)}>
            <label htmlFor="brightness">
                <Text colorScheme={colorScheme}>Brightness: </Text>
            </label>
            <input placeholder={strip.brightness.toString()} {...register("brightness")}/>
      </form>

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
});

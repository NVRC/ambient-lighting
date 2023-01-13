import { View, Text, FlatList, SafeAreaView, StyleSheet, ActivityIndicator } from 'react-native';

import EditScreenInfo from 'controller/components/EditScreenInfo';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

import { AnimationDetails, AnimationSettings } from 'controller/redux/services/ledStripsApi';
import { STRIP_ID } from 'controller/redux/store';

import { useGetStripAnimationsStripsStripIdAnimateGetQuery } from 'controller/redux/services/ledStripsApi';


type AnimationDetailsList = Array<AnimationDetails>

const animations: Array<AnimationDetails> = [
]

const AnimationTile = ({animation}: {animation: AnimationDetails}) => {
    return (
        <View>
            <Text>{animation.animation_type}</Text>
        </View>
    );
}

export default function AnimateTabScreen() {
  const { colorScheme } = useAppSelector(getSettings);

  const { data: animations, isLoading, isFetching, isError } = useGetStripAnimationsStripsStripIdAnimateGetQuery({
    stripId: STRIP_ID,
  })

  if (isLoading || isFetching || isError || animations === undefined){
    return (
        <View style={styles.container}>
            <ActivityIndicator />
        </View>
    )
  }

  return (
    <View style={styles.container}>
        <SafeAreaView>
            <FlatList
                data={animations}
                renderItem={({item}) => <AnimationTile animation={item} />}
                />

        </SafeAreaView>
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

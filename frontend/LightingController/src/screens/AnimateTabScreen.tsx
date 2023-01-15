import { View, TouchableOpacity, FlatList, SafeAreaView, StyleSheet, ActivityIndicator } from 'react-native';

import { Text as TText, View as TView } from 'controller/components/Themed';

import EditScreenInfo from 'controller/components/EditScreenInfo';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

import { AnimationDetails } from 'controller/redux/services/auto_gen/ledStripsApi';
import { STRIP_ID } from 'controller/redux/store';

import { useGetStripAnimationsStripsStripIdAnimateGetQuery, usePostStripAnimationStripsStripIdAnimatePostMutation } from 'controller/redux/services/ledStripsApi';


type AnimationDetailsList = Array<AnimationDetails>

const animations: Array<AnimationDetails> = [
]

const AnimationTile = ({animation}: {animation: AnimationDetails}) => {
    const { colorScheme } = useAppSelector(getSettings);

    const [ postAnimation ] = usePostStripAnimationStripsStripIdAnimatePostMutation();

    console.log(animation);
    const inputs = []
    for (const [k, v] of Object.entries(animation.settings)){

    }
    const onPress = () => {
        postAnimation({
            stripId: STRIP_ID,
            animationDetails: {
                animation_type: animation.animation_type,
                settings: animation.settings
            }
        })
    }

    return (
        <TouchableOpacity onPress={onPress} >
            <TView style={styles.item} colorScheme={colorScheme}>
                <TText style={styles.title} colorScheme={colorScheme}>{animation.animation_type.replaceAll('_', ' ').toLowerCase()}</TText>
            </TView>
        </TouchableOpacity>
    );
}

export default function AnimateTabScreen() {
  const { colorScheme } = useAppSelector(getSettings);

  const { data: animations, isLoading, isFetching, isError } = useGetStripAnimationsStripsStripIdAnimateGetQuery({
    stripId: STRIP_ID,
  })

  if (isLoading || isFetching || isError || animations === undefined){
    return (
        <TView colorScheme={colorScheme} style={styles.container}>
            <ActivityIndicator />
        </TView>
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
  item: {
    padding: 20,
    marginVertical: 8,
    marginHorizontal: 16
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

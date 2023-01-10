import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { Provider } from 'react-redux';

import store from 'controller/redux/store';

import Navigation from 'controller/navigation';


export default function App() {

    return (
        <Provider store={store}>
            <SafeAreaProvider>
                <Navigation />
                <StatusBar />
            </SafeAreaProvider>
        </Provider>
    );
}


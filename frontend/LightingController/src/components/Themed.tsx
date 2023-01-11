/**
 * Learn more about Light and Dark modes:
 * https://docs.expo.io/guides/color-schemes/
 */

import { Text as DefaultText, View as DefaultView, ColorSchemeName } from 'react-native';

import Colors from '../constants/Colors';

export function useThemeColor(
  theme: NonNullable<ColorSchemeName>,
  props: { light?: string; dark?: string },
  colorName: keyof typeof Colors.light & keyof typeof Colors.dark
) {

  const colorFromProps = props[theme];

  if (colorFromProps) {
    return colorFromProps;
  } else {
    return Colors[theme][colorName];
  }
}

type ThemeProps = {
  lightColor?: string;
  darkColor?: string;
  colorScheme: NonNullable<ColorSchemeName>;
};

export type TextProps = ThemeProps & DefaultText['props'];
export type ViewProps = ThemeProps & DefaultView['props'];

export function Text(props: TextProps) {
  const { style, lightColor, darkColor, colorScheme, ...otherProps } = props;
  const color = useThemeColor(colorScheme, { light: lightColor, dark: darkColor }, 'text');

  return <DefaultText style={[{ color }, style]} {...otherProps} />;
}

// export function TextInput(props: TextProps, onChange) {
//     const { style, lightColor, darkColor, colorScheme, ...otherProps } = props;
//     const color = useThemeColor(colorScheme, { light: lightColor, dark: darkColor }, 'text');

//     return <TextInput></TextInput>
// }

export function View(props: ViewProps) {
  const { style, lightColor, darkColor, colorScheme, ...otherProps } = props;
  const backgroundColor = useThemeColor(colorScheme, { light: lightColor, dark: darkColor }, 'background');

  return <DefaultView style={[{ backgroundColor }, style]} {...otherProps} />;
}

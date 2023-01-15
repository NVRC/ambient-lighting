import { useState, useRef } from 'react';

import * as THREE from 'three';

import { StyleSheet, TouchableOpacity } from 'react-native';

import { Text, View } from 'controller/components/Themed';
import { RootTabScreenProps } from '../../types';
import { useAppSelector } from 'controller/redux/hooks';
import { getSettings } from 'controller/redux/slices/settingsSlice';

import { Canvas, useFrame, ThreeElements } from '@react-three/fiber';
import { OrbitControls, Center } from '@react-three/drei'


const ALT_KEY = 18;
const CTRL_KEY = 17;
const CMD_KEY = 91;

const COLOR_SPACE_LIMIT = 255;

export function LedItem(props: ThreeElements['mesh']) {
  // This reference will give us direct access to the mesh
  const mesh = useRef<THREE.Mesh>(null!)

  // Set up state for the hovered and active state
  const [hovered, setHover] = useState(false)
  const [active, setActive] = useState(false)
  // Subscribe this component to the render-loop, rotate the mesh every frame
  useFrame((state, delta) => (mesh.current.rotation.x += delta))
  // Return view, these are regular three.js elements expressed in JSX
  return (

    <mesh
      ref={mesh}
      scale={active ? 1.5 : 1}
      onClick={(event) => setActive(!active)}
      onPointerOver={(event) => setHover(true)}
      onPointerOut={(event) => setHover(false)}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={hovered ? 'hotpink' : 'orange'} />
    </mesh>
  );
};

export default function RGBSpaceScreen({ navigation }: RootTabScreenProps<'RGBSpaceTab'>) {
  const { colorScheme } = useAppSelector(getSettings);

  // Set up state for the hovered and active state
  const [hovered, setHover] = useState(false)
  const [active, setActive] = useState(false)

  return (
    <View colorScheme={colorScheme} style={styles.container}>
      <Canvas camera={{ position: [300, 300, 300]}}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        <gridHelper
          args={[COLOR_SPACE_LIMIT, COLOR_SPACE_LIMIT / 10, "#ff0000", "#ff0000"]}
          position={[COLOR_SPACE_LIMIT / 2, 0, COLOR_SPACE_LIMIT / 2]}
          rotation={[0, 0, 0]}
        />
        <gridHelper
          args={[COLOR_SPACE_LIMIT, COLOR_SPACE_LIMIT / 10, "#00ff00", "#00ff00"]}
          position={[COLOR_SPACE_LIMIT / 2, COLOR_SPACE_LIMIT / 2, 0]}
          rotation={[Math.PI / 2, Math.PI / 2, 0]}
        />
        <gridHelper
          args={[COLOR_SPACE_LIMIT, COLOR_SPACE_LIMIT / 10, "#0000ff", "#0000ff"]}
          position={[0, COLOR_SPACE_LIMIT / 2, COLOR_SPACE_LIMIT / 2]}
          rotation={[0, 0, Math.PI / 2]}
        />
        <OrbitControls enableRotate autoRotateSpeed={5} />
      </Canvas>
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
});

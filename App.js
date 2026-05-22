import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = 'http://TU_IP:5001'; // Cambiar por IP de tu PC

export default function App() {
  const [token, setToken] = useState(null);
  const [target, setTarget] = useState('');
  const [results, setResults] = useState([]);
  
  const login = async () => {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'falconmx1', password: 'securepass123' })
    });
    const data = await response.json();
    setToken(data.access_token);
    await AsyncStorage.setItem('token', data.access_token);
  };
  
  const scanNetwork = async () => {
    const response = await fetch(`${API_URL}/api/scan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ target: target, ports: '1-1000' })
    });
    const data = await response.json();
    setResults(data.open_ports);
  };
  
  useEffect(() => {
    AsyncStorage.getItem('token').then(t => t && setToken(t));
  }, []);
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🌐 Networking Tool</Text>
      {!token ? (
        <Button title="Login" onPress={login} />
      ) : (
        <>
          <TextInput
            style={styles.input}
            placeholder="IP o dominio"
            value={target}
            onChangeText={setTarget}
          />
          <Button title="Escanear" onPress={scanNetwork} />
          <FlatList
            data={results}
            keyExtractor={(item) => item.toString()}
            renderItem={({ item }) => <Text style={styles.result}>Puerto {item} - ABIERTO</Text>}
          />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#667eea' },
  title: { fontSize: 24, color: 'white', textAlign: 'center', marginBottom: 20 },
  input: { backgroundColor: 'white', padding: 10, marginBottom: 10, borderRadius: 5 },
  result: { backgroundColor: '#00b894', color: 'white', padding: 10, marginTop: 5, borderRadius: 5 }
});

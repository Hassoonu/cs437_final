import { useState, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  StatusBar,
  ActivityIndicator,
} from 'react-native';
import { initializeApp, getApps } from 'firebase/app';
import { getDatabase, ref, onValue, get } from 'firebase/database';

const firebaseConfig = {
  apiKey: "AIzaSyCi_pRHNVqZkbcKZgatNENXsqBufsGnOA0",
  authDomain: "final-fe519.firebaseapp.com",
  databaseURL: "https://final-fe519-default-rtdb.firebaseio.com", 
  projectId: "final-fe519",
  storageBucket: "final-fe519.firebasestorage.app",
  messagingSenderId: "757688929699",
  appId: "1:757688929699:web:6a5e2083404b8ac7289e16"
};

type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error';
 
export default function Index() {
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');
  const [needsWater, setNeedsWater] = useState<boolean | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
 
  // Stored so the refresh button can re-query without reconnecting
  const plantRefStore = useRef<any>(null);
 
  const handleConnect = () => {
    setStatus('connecting');
    setErrorMsg(null);
 
    try {
      const app = getApps().length === 0
        ? initializeApp(firebaseConfig)
        : getApps()[0];
 
      const db = getDatabase(app);
      const plantRef = ref(db, 'Hasan/money_tree');
      plantRefStore.current = plantRef;
 
      onValue(
        plantRef,
        (snapshot) => {
          const data = snapshot.val();
          console.log('Firebase data on connect:', JSON.stringify(data));
          setNeedsWater(!!data?.needs_water);
          setStatus('connected');
        },
        (error) => {
          setErrorMsg(error.message);
          setStatus('error');
        },
        { onlyOnce: true }  // one-time read on connect; refresh handles subsequent pulls
      );
    } catch (e: any) {
      setErrorMsg(e?.message ?? 'Unknown error');
      setStatus('error');
    }
  };
 
  const handleRefresh = async () => {
    if (!plantRefStore.current) return;
    setRefreshing(true);
    setErrorMsg(null);
    try {
      const snapshot = await get(plantRefStore.current);
      const data = snapshot.val();
      console.log('Firebase data on refresh:', JSON.stringify(data));
      setNeedsWater(!!data?.needs_water);
    } catch (e: any) {
      setErrorMsg(e?.message ?? 'Refresh failed');
    } finally {
      setRefreshing(false);
    }
  };
 
  // ── Derived display values ──────────────────────────────────────
  console.log('needsWater state on render:', needsWater);
  const statusLine = (() => {
    if (status === 'connected') {
      const label = needsWater ? 'Needs Watering 💧' : 'Ok!';
      return { top: 'Connected', bottom: `Status: ${label}`, isConnected: true };
    }
    if (status === 'error') {
      return { top: null, bottom: 'Connection failed. Try again.', isConnected: false };
    }
    return { top: null, bottom: 'Not connected to plant', isConnected: false };
  })();
 
  const buttonLabel = (() => {
    if (status === 'connecting' || refreshing) return null; // shows spinner
    if (status === 'connected') return 'Refresh';
    if (status === 'error') return 'Retry Connection';
    return 'Connect to Plant';
  })();
 
  const buttonDisabled = status === 'connecting' || refreshing;
  // ───────────────────────────────────────────────────────────────
 
  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FEF0E3" />
 
      <View style={styles.card}>
        {/* Status box */}
        <View style={[
          styles.statusBox,
          statusLine.isConnected && styles.statusBoxConnected,
          status === 'error' && styles.statusBoxError,
        ]}>
          {statusLine.top && (
            <Text style={styles.statusConnectedLabel}>{statusLine.top}</Text>
          )}
          <Text style={[
            styles.statusText,
            !statusLine.isConnected && styles.statusTextMuted,
          ]}>
            {statusLine.bottom}
          </Text>
        </View>
 
        {/* Connect / Refresh button */}
        <TouchableOpacity
          style={[
            styles.button,
            buttonDisabled && styles.buttonDisabled,
            status === 'error' && styles.buttonError,
          ]}
          onPress={status === 'connected' ? handleRefresh : handleConnect}
          disabled={buttonDisabled}
          activeOpacity={0.75}
        >
          {status === 'connecting' || refreshing ? (
            <ActivityIndicator color="#fff" size="small" />
          ) : (
            <Text style={styles.buttonText}>{buttonLabel}</Text>
          )}
        </TouchableOpacity>
 
        {/* Error detail — shows actual Firebase error message for debugging */}
        {errorMsg && (
          <Text style={styles.errorMsg}>{errorMsg}</Text>
        )}
      </View>
    </View>
  );
}
 
// ── Palette ──────────────────────────────────────────────────────
// Background: warm parchment (#FEF0E3)
// Accent:     terracotta  (#D97040)
// Card:       white with soft warm shadow
// ─────────────────────────────────────────────────────────────────
 
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FEF0E3',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 28,
  },
 
  // Card
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 28,
    paddingVertical: 40,
    paddingHorizontal: 32,
    alignItems: 'center',
    width: '100%',
    shadowColor: '#C97B3A',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.13,
    shadowRadius: 28,
    elevation: 10,
  },
 
  // Status display
  statusBox: {
    backgroundColor: '#FDF5EE',
    borderRadius: 16,
    paddingVertical: 18,
    paddingHorizontal: 24,
    alignItems: 'center',
    width: '100%',
    marginBottom: 24,
    borderWidth: 1.5,
    borderColor: '#EDD9C4',
    minHeight: 72,
    justifyContent: 'center',
  },
  statusBoxConnected: {
    borderColor: '#D97040',
    backgroundColor: '#FFF8F2',
  },
  statusBoxError: {
    borderColor: '#E0A090',
    backgroundColor: '#FFF5F3',
  },
  statusConnectedLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: '#D97040',
    letterSpacing: 2,
    textTransform: 'uppercase',
    marginBottom: 6,
  },
  statusText: {
    fontSize: 18,
    fontWeight: '700',
    color: '#2E1F0F',
    textAlign: 'center',
  },
  statusTextMuted: {
    color: '#B09080',
    fontWeight: '500',
    fontSize: 16,
  },
 
  // Button
  button: {
    backgroundColor: '#D97040',
    borderRadius: 16,
    paddingVertical: 17,
    width: '100%',
    alignItems: 'center',
    shadowColor: '#D97040',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 6,
  },
  buttonDisabled: {
    backgroundColor: '#C8A882',
    shadowOpacity: 0,
    elevation: 0,
  },
  buttonError: {
    backgroundColor: '#C05A3A',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.4,
  },
  errorMsg: {
    marginTop: 14,
    fontSize: 12,
    color: '#C05A3A',
    textAlign: 'center',
    lineHeight: 18,
  },
});
 
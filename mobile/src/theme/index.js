/**
 * App Theme Configuration
 */

import { MD3LightTheme as DefaultTheme } from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#4CAF50', // Green for agriculture
    secondary: '#FF9800', // Orange for alerts
    tertiary: '#2196F3', // Blue for blockchain
    background: '#F5F5F5',
    surface: '#FFFFFF',
    error: '#F44336',
    success: '#4CAF50',
    warning: '#FFC107',
    info: '#2196F3',
    text: '#212121',
    textSecondary: '#757575',
    border: '#E0E0E0',
  },
  roundness: 8,
  fonts: {
    ...DefaultTheme.fonts,
    regular: {
      fontFamily: 'System',
      fontWeight: '400',
    },
    medium: {
      fontFamily: 'System',
      fontWeight: '500',
    },
    bold: {
      fontFamily: 'System',
      fontWeight: '700',
    },
  },
};

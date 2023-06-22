import * as React from 'react';
import * as ReactDOM from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import App from './App';
import Info from './Info';
import { red } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';
import { BrowserRouter, Routes, Route, } from "react-router-dom";

// A custom theme for this app
const theme = createTheme({
  palette: {
    primary: {
      main: '#556cd6',
    },
    secondary: {
      main: '#19857b',
    },
    error: {
      main: red.A400,
    },
  },
});

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
  <ThemeProvider theme={theme}>
    {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
    <CssBaseline />

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="info" element={<Info />} />
      </Routes>
    </BrowserRouter>

  </ThemeProvider>,
);
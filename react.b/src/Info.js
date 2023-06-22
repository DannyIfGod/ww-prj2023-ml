import { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Container from '@mui/material/Container';
import Alert from '@mui/material/Alert';
import Grid from '@mui/material/Unstable_Grid2'; // Grid version 2

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

//const AllSupportedSyptoms = ["Sym1", "Sym2", "Sym3", "Sym4", "Sym5"];
const backendBaseUrl = "http://127.0.0.1:5000"



// Info page
function Info() {

  // Container that holds all the text and home botton
  return (
    <Container maxWidth="xl">

      <Grid container direction="column" justifyContent="flex-start" alignItems="center" spacing={2}>
        
        <Grid container direction="row" spacing={1} justifyContent="flex-start" alignItems="baseline">

          <Grid>
            <h1>Info</h1>
          </Grid>

          <Grid>
            <Button variant="outlined" href="/" size="small" >Home</Button>
          </Grid>

        </Grid>

        <Grid justifyContent="center">
          <h3>How To Use</h3>
          <div>1. Click on the drop-down menu and select any symptom.</div>
          <div>2. Click the Add button to add another drop-down menu to select another symptom.</div>
          <div>3. Click the Remove button to remove a drop-down menu.</div>
          <div>4. Make sure that every drop-down menu has a symptom before the generation.</div>
          <div>5. Click generate to produce a result.</div>
          <div>6. The result will be a percentage which means the ammount of classifiers aggreing with ur diagnoses.</div>
        </Grid>

        <Grid justifyContent="center">
            <h3>How It Works</h3>
            <div>My program uses Machine learning to diagnose certain inputed symptoms from the user. I have decided to use the three classifiers, Random Forest Classifier, Support Vector Classifier, and Gaussian Naive Bayes Classifier. </div>
        </Grid>

      </Grid>
    </Container>
  );
}

export default Info;

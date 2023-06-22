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
const MAX_SYMPTOMS_COUNT = 8;



// Home page
function App() {
  const [symptoms, setSymptoms] = useState([]);
  const [alertText, setAlertText] = useState();
  const [alertMode, setAlertMode] = useState("success");
  const [AllSupportedSyptoms, setAllSupportedSyptoms] = useState([]);
  const [results, setResults] = useState();



  // fetchSymptomsList function returns a json with all the symmptoms
  const fetchSymptomsList = () => {
    fetch(`${backendBaseUrl}/symptoms`)
      .then(response => {
        return response.json()
      })
      .then(data => {
        setAllSupportedSyptoms(data)
      })
  }



  // fetchSymptomsList function returns a json with all the symmptoms
  const fetchDignoseResult = (symps) => {
    fetch(`${backendBaseUrl}/generate/${symps}`)
      .then(response => {
        return response.json()
      })
      .then(data => {
        setAlertText(JSON.stringify(data, null, 4))
        const l = data.diseases.length
        const percent = 1 / l;
        const d = {}
        data.diseases.forEach(i => {
          if (d[i]) {
            d[i] += percent
          } else {
            d[i] = percent
          }
        });

        setResults(d);
        console.log("results:", d)
      })
  }



  // useEffect() is called when the page needs to be re-rendered
  useEffect(() => {
    fetchSymptomsList()
    if (symptoms.length === 0) {
      setSymptoms([-1]);
    }
  }, [symptoms.length]);



  // onSelectSymptom function adds the selected symptom from user to an array
  const onSelectSymptom = (index, e) => {
    const v = e.target.value;
    const exist = symptoms.find(i => i === v);
    if (exist) {
      alert(`${AllSupportedSyptoms[v]} is already chosen!`)
      return;
    }
    const newsymp = [...symptoms];
    newsymp[index] = v;
    setSymptoms(newsymp);
    setResults()
    setAlertText()
  }



  // onAddSymptoms function that adds a drop-down menu when user clicks "add" button
  const onAddSymptoms = () => {
    if (symptoms.length < MAX_SYMPTOMS_COUNT) {
      const newsymp = [...symptoms];
      newsymp.push(-1)
      setSymptoms(newsymp);
      setAlertText()
    } else {
      setAlertText(`Max of ${MAX_SYMPTOMS_COUNT} symptoms!`)
      setAlertMode("error")
      return;
    }
  }



  // onDeleteSymptoms function that deletes a drop-down menu when user clicks "delete" button
  const onDeleteSymptoms = () => {
    const newsymp = [...symptoms];
    newsymp.pop()
    setSymptoms(newsymp);
    setAlertText()
  }



  // onSubmit function that returns the diagnostic when user clicks "generate" button
  const onSubmit = () => {
    const exist = symptoms.find(i => i < 0);
    if (exist) {
      //alert("Please choose all the symptoms first!")
      setAlertText("Please choose all the symptoms first!")
      setAlertMode("error")
      return;
    };

    const ss = symptoms.map(i => AllSupportedSyptoms[i]);

    fetchDignoseResult(ss)

    //setAlertText(`${ss}`)
    //setAlertMode("success")

  }



  // renderSymptomDropdown function is what puts the drop-down menus into display
  // so the user can see it
  const renderSymptomDropdown = (value, index) => {
    const label = "Please select symptom";
    const id = `select-${index}`;
    const labelid = `select-label-${index}`;
    return (
      <Grid container>
        <FormControl required sx={{ m: 1, minWidth: 200 }} size="small">
          <InputLabel id={labelid}>{label}</InputLabel>
          <Select
            labelId={labelid}
            id={id}
            value={value}
            label={label}
            onChange={(e) => { onSelectSymptom(index, e); }}
          >
            {
              AllSupportedSyptoms.map((s, i) => {
                return <MenuItem value={i}>{s}</MenuItem>
              })
            }
          </Select>
        </FormControl>
      </Grid>
    )
  }



  // Container that contains and displays all the drop-down menus, add button, remove button...
  return (
    <Container maxWidth="xl">
      <Grid container direction="column" justifyContent="flex-start" alignItems="center" spacing={2}>
        <Grid container direction="row" spacing={1} justifyContent="flex-start" alignItems="baseline">
          <Grid>
            <h2>An AI Doctor Demo</h2>
          </Grid>
          <Grid>
            <Button variant="outlined" href="info" size="small" >Info</Button>
          </Grid>
        </Grid>
        <Grid>
          <h3>1. Choose the Symptoms</h3>
        </Grid>
        <Grid container direction="row" spacing={6}>
          <Grid container direction="column" alignItems="flex-start" spacing={2}>
            {
              symptoms.map((i, j) => renderSymptomDropdown(i, j))
            }
          </Grid>
          <Grid container direction="column" justifyContent="flex-start" alignItems="flex-start" spacing={2}>
            <Grid>
              <Button variant="contained" onClick={onAddSymptoms}>Add</Button>
            </Grid>
            {
              symptoms.length > 1 && <Grid>
                <Button variant="contained" onClick={onDeleteSymptoms}>Delete</Button>
              </Grid>
            }
          </Grid>
        </Grid>
        <Grid>
          <h3>2. Click Diagnose to generate the results</h3>
        </Grid>
        <Grid>
          <Button type="submit" variant="outlined" onClick={onSubmit}>Diagnose</Button>
        </Grid>
        {results && <Grid>
          <List
            sx={{
              width: '100%',
              maxWidth: 360,
              bgcolor: 'background.paper',
              position: 'relative',
              overflow: 'auto',
              maxHeight: 300,
              '& ul': { padding: 0 },
            }}
            subheader={<li />}
          >
            {Object.keys(results).map(i => {
              return <ListItem key={`item-${i}`}>
                <ListItemText primary={`${i} - ${(results[i] * 100).toFixed(2)}%`} />
              </ListItem>
            })}
          </List>

        </Grid>}
        <Grid>
          {alertText && <Alert severity={alertMode}>
            {alertText}
          </Alert>}
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;

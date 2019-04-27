import React from 'react';
import logo from './logo.svg';
import './App.css';




class Word extends React.Component{
  constructor(props){
    super(props);
    // const data = this.props.data.word;
    this.state = {
      word: props.data.word
    }
  }

  change = (evt)=>{
    this.setState({word: this.props.data.value})
  }

  reset = (evt)=>{
    this.setState({word: this.props.data.word})
  }

  render(){
    return (<span onMouseEnter={this.change} onMouseLeave={this.reset} className={"word "+ this.props.data.label}>{this.state.word}</span>);
  }
}

class Row extends React.Component{
  constructor(){
    super();
    this.state = {
    }
  }

  render(){
    const sentence = this.props.data.map((value, idx)=>(<Word data = {value} key={idx}/>));
    return (<span className={"row"}>{sentence}</span>);
  }
}

class MyTable extends React.Component{
  constructor(){
    super();
    this.state = {
      data : [],
      line: "",
      url: ""
    }
  }

  readInput = (evt)=>{
    const file = evt.target.files[0];
    const fileReader = new FileReader();
    fileReader.readAsText(file);
    fileReader.onload = (evt) => this.setState({data: JSON.parse(fileReader.result)});

  }
  ReadFile = ()=>{
   return (<input type="file" onInput={this.readInput}></input>)
  }

  readLine = (evt)=>{
    this.setState({line: evt.target.value.trim()});
  }

  getResult = (evt)=>{
    evt.preventDefault();
    if(this.state.line.trim().length == 0) return
    const res = [
      {
          "word": "Hey",
          "label": "positive",
          "value": 0.564
      },
      {
          "word": "I",
          "label": "positive",
          "value": 0.564
      },
      {
          "word": "am",
          "label": "positive",
          "value": 0.564
      },
      {
          "word": "good",
          "label": "positive",
          "value": 0.564
      }
  ];
  fetch(this.state.url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, cors, *same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
        "Content-Type": "application/json",
        // "Content-Type": "application/x-www-form-urlencoded",
    },
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    body: JSON.stringify({line: this.state.line}), // body data type must match "Content-Type" header
  }).then((res)=>{
    console.log(res);
  });
  const arr = this.state.data.slice();
  arr.push(res);
  this.setState({data: arr});
  }

  TakeInput = ()=>{
    return (<div>
      <form onSubmit={this.getResult}> 
        <input type="text" onChange={this.readLine} />
        <input type="submit" value="submit"/>
      </form>
      </div>);
  }

  urlChange = (evt)=>{
    this.setState({url: evt.target.value.trim()});
  }

  saveData = (evt)=>{
    
  }

  render() {
    const rows = this.state.data.reverse().map((value, idx)=>(<div className="line" key={idx} ><Row data = {value}/></div>));
    return (
      <div>
        <input type="text" onChange={this.urlChange}/>
        <this.TakeInput/>
        <br/>
        <this.ReadFile/>
        <br/>
        {rows}
        <br/>
        <input type="button" value="save" onClick={this.saveData} />
      </div>
    )
  }
}

function App() {
  return (
    <div className="App">
      <MyTable />
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;

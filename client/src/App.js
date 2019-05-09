import React from 'react';
import logo from './logo.svg';
import './App.css';




class Mapping extends React.Component{
  constructor(props){
    super(props);
    // const data = this.props.data.word;
    this.state = {
      // word: props.data.word
    }
  }

  render(){
    const arr = [];
    // console.log(this.props);
    for(const x in this.props.data){
      // const score = (<span class="score"> {this.props.data.score} </span>);
      if(!x.length) continue;
      const label = (Number(this.props.data[x]['score']) > 0)?"positive":"negative";
      for(const y of this.props.data[x]["targets"]){
        if(!y.length) continue;
        arr.push((<span class={"mapping "+label}><span class="x">{x}</span> &rarr; <span class="y">{y}</span></span>));
      }
    }
    return (<div>{arr}</div>);
    // return (<span onMouseEnter={this.change} onMouseLeave={this.reset} className={"word "+ this.props.data.label}>{this.state.word}</span>);
  }
}

class Row extends React.Component{
  constructor(){
    super();
    this.state = {
    }
  }

  render(){
    const result = this.props.data.result;
    const sentence = this.props.data.sentence;
    return (<div><span class={"sentence"}> {sentence} </span><br/><Mapping data = {result}/></div>);
  }
}

class MyTable extends React.Component{
  constructor(){
    super();
    let res = window.localStorage.getItem('data');
    if(res==null){
      window.localStorage.setItem("data", JSON.stringify([]));
    }
    res = JSON.parse(window.localStorage.getItem('data'));
    this.state = {
      data : res,
      line: "",
      url: "http://localhost/text/"
    }
    
  }

  // readInput = (evt)=>{
  //   const file = evt.target.files[0];
  //   const fileReader = new FileReader();
  //   fileReader.readAsText(file);
  //   fileReader.onload = (evt) => this.setState({data: JSON.parse(fileReader.result)});

  // }
  // ReadFile = ()=>{
  //  return (<input type="file" onInput={this.readInput}></input>)
  // }

  readLine = (evt)=>{
    this.setState({line: evt.target.value.trim()});
  }

  getResult = (evt)=>{
    evt.preventDefault();
    if(this.state.line.trim().length == 0) return
    // const res = {"sentence": "toilet are bad", "result": {"toilet": {"targets": ["bad"], "score": "-2.000000"}}};

    

  //   fetch(this.state.url+this.state.line, {
  //   method: "GET", // *GET, POST, PUT, DELETE, etc.
  //   mode: "cors", // no-cors, cors, *same-origin
  //   // cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
  //   credentials: "same-origin", // include, *same-origin, omit
  //   // headers: {
  //   //     "Content-Type": "application/json",
  //   //     // "Content-Type": "application/x-www-form-urlencoded",
  //   // },
  //   // redirect: "follow", // manual, *follow, error
  //   // referrer: "no-referrer", // no-referrer, *client
  //   // body: JSON.stringify({line: this.state.line}), // body data type must match "Content-Type" header
  // })
  // fetch("http://localhost/text/toilets%20stink%20and%20basin%20leak%20water", 
  fetch(this.state.url+this.state.line, {"headers":{"accept":"application/json","cache-control":"no-cache","pragma":"no-cache","upgrade-insecure-requests":"1"},"referrerPolicy":"no-referrer-when-downgrade","method":"GET","dataType": "jsonp"})
  .then((r)=>{
    r.json().then((res)=>{
      const arr = this.state.data.slice();
      arr.push(res);
    // console.log(arr);
    this.setState({data: arr});
    console.log(arr);
    window.localStorage.setItem("data", JSON.stringify(arr));
    });
  });
    // const arr = this.state.data.slice();
    // arr.push(res);
    // console.log(arr);
    // this.setState({data: arr});
    // console.log(JSON.stringify(this.state.data))
    // window.localStorage.setItem("data", JSON.stringify(arr));
  }

  TakeInput = ()=>{
    return (<div>
      <form onSubmit={this.getResult}> 
        <input type="text" onChange={this.readLine} />
        <input type="submit" value="submit"/>
      </form>
      </div>);
  }

  // urlChange = (evt)=>{
  //   this.setState({url: evt.target.value.trim()});
  // }

  // saveData = (evt)=>{
    
  // }

  render() {
    const rows = this.state.data.map((value, idx)=>
      (<div className="line" key={idx} ><Row data = {value}/></div>)
    );
    return (
      <div>
        {/* <input type="text" onChange={this.urlChange}/> */}
        <this.TakeInput/>
        <br/>
        {/* <this.ReadFile/> */}
        <br/>
        {rows}
        <br/>
        {/* <input type="button" value="save" onClick={this.saveData} /> */}
      </div>
    )
  }
}

function App() {
  return (
    <div className="App">
    <h1>Sentiment Analyzer</h1>
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

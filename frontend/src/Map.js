import React, { Component } from 'react';
import { Map, GoogleApiWrapper, Polygon, Marker } from 'google-maps-react';
import axios from 'axios';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import CardActions from '@material-ui/core/CardActions';


const mapStyles = [
  {
    elementType: "geometry",
    stylers: [
      {
        color: "#f5f5f5"
      }
    ]
  },
  {
    elementType: "labels.icon",
    stylers: [
      {
        visibility: "off"
      }
    ]
  },
  {
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#616161"
      }
    ]
  },
  {
    elementType: "labels.text.stroke",
    stylers: [
      {
        color: "#f5f5f5"
      }
    ]
  },
  {
    featureType: "administrative.land_parcel",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#bdbdbd"
      }
    ]
  },
  {
    featureType: "poi",
    elementType: "geometry",
    stylers: [
      {
        color: "#eeeeee"
      }
    ]
  },
  {
    featureType: "poi",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#757575"
      }
    ]
  },
  {
    featureType: "poi.park",
    elementType: "geometry",
    stylers: [
      {
        color: "#e5e5e5"
      }
    ]
  },
  {
    featureType: "poi.park",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#9e9e9e"
      }
    ]
  },
  {
    featureType: "road",
    elementType: "geometry",
    stylers: [
      {
        color: "#ffffff"
      }
    ]
  },
  {
    featureType: "road.arterial",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#757575"
      }
    ]
  },
  {
    featureType: "road.highway",
    elementType: "geometry",
    stylers: [
      {
        color: "#dadada"
      }
    ]
  },
  {
    featureType: "road.highway",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#616161"
      }
    ]
  },
  {
    featureType: "road.local",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#9e9e9e"
      }
    ]
  },
  {
    featureType: "transit.line",
    elementType: "geometry",
    stylers: [
      {
        color: "#e5e5e5"
      }
    ]
  },
  {
    featureType: "transit.station",
    elementType: "geometry",
    stylers: [
      {
        color: "#eeeeee"
      }
    ]
  },
  {
    featureType: "water",
    elementType: "geometry",
    stylers: [
      {
        color: "#c9c9c9"
      }
    ]
  },
  {
    featureType: "water",
    elementType: "labels.text.fill",
    stylers: [
      {
        color: "#9e9e9e"
      }
    ]
  }
];

function mkCoordinate(lat, lng) {
  return (
    {
      lat: lat,
      lng: lng
    }
  )
}

function mkBox(coordinate, width, height) {
  const deltaLat = -height/111
  const deltaLng = width/111
  return (
    [
      {lat: coordinate.lat, lng: coordinate.lng},
      {lat: coordinate.lat, lng: coordinate.lng + deltaLng},
      {lat: coordinate.lat + deltaLat, lng: coordinate.lng + deltaLng},
      {lat: coordinate.lat + deltaLat, lng: coordinate.lng}
    ]
  )
}

function mkBoxPolygon(box, fill="#F596AA", stroke="#D0104C", opacity=0.2) {
  return (
    <Polygon
      paths={box}
      strokeColor={stroke}
      strokeOpacity={1}
      strokeWeight={2}
      fillColor={fill}
      fillOpacity={opacity}
    />
  )
}

function mkMarker(coordinate, label) {
  return (
    <Marker
      label={label}
      position={coordinate}
      icon={"None"}
    />  
  )
}
 
function mkGrid(coordinate, width, height, rows, cols) {
  const boxes = []
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const latOffset = -height * row / 111;
      const lngOffset = width * col / 111;
      const boxCoordinate = mkCoordinate(coordinate.lat + latOffset, coordinate.lng + lngOffset)
      boxes.push(mkBox(boxCoordinate, width, height))
    }
  }
  return boxes;
}

function mkGridPolygon(boxes) {
  console.log(boxes)
  const polygons = []
  for (let i = 0; i < boxes.length; i++) {
    polygons.push(mkBoxPolygon(boxes[i]))
  }
  return polygons
}

function mkGridMarker(boxes, labels, labelVerticalOffset=0.01) {
  const markers = []
  for (let i = 0; i < boxes.length; i++) {
    const markerCoordinate = mkCoordinate(
      -labelVerticalOffset + boxes[i][0].lat + (boxes[i][2].lat - boxes[i][0].lat)/2, 
      boxes[i][1].lng + (boxes[i][3].lng - boxes[i][1].lng)/2
    )
    markers.push(mkMarker(markerCoordinate, labels[i]))
  }
  return markers
}


export class MapContainer extends Component {
  state = {
    melbGridLabels: ["Loading", "Loading"],
    sydGridLabels: ["Loading", "Loading"],
    sydAurin: [],
    sydScore: [],
    sydLabel: [],
    melbAurin: [],
    melbScore: [],
    melbLabel: [],
    description: "Loading",
    title: "Loading",
    dataLabel: "Loading",
    showingAurin: true,
    buttonLabel: "Toggle Data"
  }

  componentDidMount() {
    axios.get(`http://127.0.0.1:5000/data`)
      .then(res => {
        console.log(res.data)
        const sydAurin = res.data["sydney"]["aurin"]
        const sydScore = res.data["sydney"]["score"]
        const sydLabel = res.data["sydney"]["labels"]
        const sydResult = []

        for (let i = 0; i < sydAurin.length; i++) {
          sydResult.push(`${sydLabel[i]}: ${sydAurin[i]}`)
        }

        const melbAurin = res.data["melbourne"]["aurin"]
        const melbScore = res.data["melbourne"]["score"]  
        const melbLabel = res.data["melbourne"]["labels"]
        const melbResult = []

        for (let i = 0; i < melbAurin.length; i++) {
          melbResult.push(`${melbLabel[i]}: ${melbAurin[i]}`)
        }
        
        this.setState({
          melbGridLabels: sydResult,
          sydGridLabels: melbResult,
          sydAurin: sydAurin,
          sydScore: sydScore,
          sydLabel: sydLabel,
          melbAurin: melbAurin,
          melbScore: melbScore,
          melbLabel: melbLabel,
          description: res.data["description"],
          dataLabel: res.data["data_name"],
          title: res.data["title"]
        })
      })
  }

  switchData = () => {
    const sydResult = []
    const melbResult = []
    const showingAurin = !this.state.showingAurin
    console.log(this.state.sydScore)
    if (showingAurin) {
      for (let i = 0; i < this.state.sydScore.length; i++) {
        sydResult.push(`${this.state.sydLabel[i]}: ${this.state.sydAurin[i]}`)
      }
      for (let i = 0; i < this.state.melbScore.length; i++) {
        melbResult.push(`${this.state.melbLabel[i]}: ${this.state.melbAurin[i]}`)
      }
    } else {
      for (let i = 0; i < this.state.sydAurin.length; i++) {
        sydResult.push(`${this.state.sydLabel[i]}: ${this.state.sydScore[i]}`)
      }
      for (let i = 0; i < this.state.melbAurin.length; i++) {
        melbResult.push(`${this.state.melbLabel[i]}: ${this.state.melbScore[i]}`)
      }
    }

    this.setState({
      melbGridLabels: sydResult,
      sydGridLabels: melbResult,
      showingAurin: showingAurin
    })
  }

  render() {
    // const [melbGridLabels, setMelbGridLabels] = useState(["Loading", "Loading"]);
    // const [sydGridLabels, setSydGridLabels] = useState(["Loading", "Loading"]);

    const melbCoordinate = mkCoordinate(-37.81516575817448, 144.96498003350143);
    const melbBoundCoordinate = mkCoordinate(-37.5112737225, 144.593741856);
    const melbGridRows = 1;
    const melbGridCols = 1;
    const melbBoxWidth = 101.2; // Kilometers
    const melbBoxHeight = 101.2; // Kilometers
    const melbGrid = mkGrid(melbBoundCoordinate, melbBoxWidth, melbBoxHeight, melbGridRows, melbGridCols);
    const melbGridPolygon = mkGridPolygon(melbGrid)
    const melbGridMarker = mkGridMarker(melbGrid, this.state.melbGridLabels);

    const sydCoordinate = mkCoordinate(-33.86751670912247, 151.10226876034878);
    const sydBoundCoordinate = mkCoordinate(-33.51422371695108, 150.76740270605987);
    const sydGridRows = 1;
    const sydGridCols = 1;
    const sydBoxWidth = 40; // Kilometers
    const sydBoxHeight = 40; // Kilometers
    const sydGrid = mkGrid(sydBoundCoordinate, sydBoxWidth, sydBoxHeight, sydGridRows, sydGridCols);
    const sydGridPolygon = mkGridPolygon(sydGrid)
    const sydGridMarker = mkGridMarker(sydGrid, this.state.sydGridLabels);

    


    return (
      <div>
        
        <Map
          google={this.props.google}
          zoom={9}
          disableDefaultUI
          styles={mapStyles}
          initialCenter={melbCoordinate}
          style={{width: '50%', height: '100%', marginLeft: "0%", zIndex:"1", borderRight:"thick solid #FFFFFF"}}
        >
          {melbGridMarker}
          {melbGridPolygon}
        </Map>
        
        <Map
            google={this.props.google}
            zoom={9}
            disableDefaultUI
            styles={mapStyles}
            initialCenter={sydCoordinate}
            style={{width: '50%', height: '100%', marginLeft: "50%", zIndex:"1", borderLeft:"thick solid #FFFFFF"}}
          >
            {sydGridMarker}
            {sydGridPolygon}
        </Map>
        <div style={{ width:"100%", padding: "10px", position: "absolute", zIndex:"2"}}>
          <Grid container xs={6} spacing={2}
            direction="column"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              <Card style={{width:500}}>
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    {this.state.title}
                  </Typography>
                  <Typography color="body" gutterBottom>
                    {this.state.description}
                  </Typography>
                </CardContent>
                <CardActions>
                <Button color="primary" size="small" onClick={this.switchData}>
                  {this.state.buttonLabel}
                </Button>
                <Button size="small" disabled style={{color:"#DB4D6D"}}>
                    Currently showing {this.state.showingAurin ? "AURIN" : this.state.dataLabel} data
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          </Grid>  
        </div>
        
      </div>

    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyCctaZGMPKzjSlb7TgpDqR7AFXmRdxNngY'
})(MapContainer);
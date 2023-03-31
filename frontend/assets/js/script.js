// ------------------------------
// Searching and Displaying Photos
// ------------------------------

var name = '';
var encoded = null;
var fileExt = null;
var SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();
const icon = document.querySelector('i.fa.fa-microphone');

const search = document.querySelector(".search-box input"),
images = document.querySelectorAll(".image-box");

function voiceToText() {
  recognition.start();
  recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    console.log(speechToText);
    search.value = speechToText;
    
    var params = {q: search.value.toLowerCase()};
    var additionalParams = {headers: {
      'Content-Type':"application/json"
    }};

    return searchApiCall(params, {}, additionalParams);
  }
}

search.addEventListener("keyup", () =>{
if(search.value != "") return;

images.forEach(image =>{
  image.style.display = "block";
})
})

search.addEventListener("keyup", e =>{
  if(e.key == "Enter"){
    let searchValue = search.value,
    value = searchValue.toLowerCase();

    var body = {};
    var params = {q : value};
    var additionalParams = {headers: {
      'Content-Type':"application/json"
    }};

    return searchApiCall(params, body, additionalParams);
  }
});

function searchApiCall(params, body, additionalParams) {
  // clean up from last search by removing old photos
  // var elem = document.getElementsByClassName("image-box")
  // elem.parentNode.removeChild(elem);

  var sdk = apigClientFactory.newClient({});

  return sdk.searchGet(params, body , additionalParams).then(function(res){
    console.log("success");
    console.log(res);
    displayImages(res.data)
  }).catch(function(result){
      console.log(result);
      console.log("NO RESULT");
  });
}

function displayImages(result) {
  var results=result.body.imagePaths

  var imageContainer = document.getElementById("image-container");
  for (var i = 0; i < results.length; i++) {
    var newimg = document.createElement("div");
    newimg.className = "image-box";

    var source = document.createElement("img");
    source.src = results[i];
    
    newimg.appendChild(source);
    imageContainer.appendChild(newimg);
  }
}

// ------------------------------
// Uploading Images
// ------------------------------

const fileButton = document.getElementById("image-file");

function uploadImage() {
  fileButton.click(); 
}

function previewFile(input) {
  var reader = new FileReader();
  photo = input.files[0].name;
  fileExt = photo.split(".").pop();
  
  console.log("Extension type: ", fileExt);

  var onlyname = photo.replace(/\.[^/.]+$/, "");
  var finalName = onlyname+"."+fileExt;
  photo = finalName;

  reader.onload = function (e) {
    var src = e.target.result;    
    var newImage = document.createElement("img");
    newImage.src = src;
    encoded = newImage.outerHTML;

    last_index_quote = encoded.lastIndexOf('"');
    if (fileExt == 'jpg' || fileExt == 'jpeg' || fileExt == 'png') {
      encodedStr = encoded.substring(33, last_index_quote);
    }
    else {
      encodedStr = encoded.substring(32, last_index_quote);
    }
    var sdk = apigClientFactory.newClient({});

    var params = {
        "filename": photo,
        "bucket": "smartphoto-b2",
        "Content-Type": "*/*",
    };

    var additionalParams = {
      headers: {
        "Content-Type": "*/*",
        'Access-Control-Allow-Origin': '*',
      }
    };

    sdk.uploadBucketFilenamePut(params, encodedStr, additionalParams)
      .then(function (result) {
        console.log(result);
        console.log('success OK');
        alert("Photo Uploaded Successfully");
      }).catch(function (result) {
        console.log(result);
      });
    }
   reader.readAsDataURL(input.files[0]);
}
"use strict";
 var url = 'http://127.0.0.1:5000/save_audio';
 
class App {
  constructor () {
    this.btnRecord = document.getElementById('btn-record');
    this.btnStop = document.getElementById('btn-stop');

    this.debugTxt = document.getElementById('debug-txt')

    this.recordingsCont = document.getElementById('recordings-cont')

    this.isRecording = false
    this.saveNextRecording = false

    this.debugTxt.innerHTML = "остановлено"
  }

  init () {
    this._initEventListeners()
  }

  _initEventListeners () {

    this.btnRecord.addEventListener('click', evt => {
      this._stopAllRecording()
      this.saveNextRecording = true
      this._startRecording()

      this.btnRecord.disabled = true
      this.btnStop.disabled = false
      this.debugTxt.innerHTML = "запись..."
    })

    this.btnStop.addEventListener('click', evt => {
      this._stopAllRecording();

      this.btnRecord.disabled = false
      this.btnStop.disabled = true
      this.debugTxt.innerHTML = "остановлено"
    })
  }

  _startRecording () {
    if (!this.recorderSrvc) {
      this.recorderSrvc = new RecorderService()
      this.recorderSrvc.em.addEventListener('recording', (evt) => this._onNewRecording(evt))
    }

    if (!this.webAudioPeakMeter) {
      this.webAudioPeakMeter = new WebAudioPeakMeter()
      this.meterEl = document.getElementById('recording-meter')
    }

    this.recorderSrvc.onGraphSetupWithInputStream = (inputStreamNode) => {
      this.meterNodeRaw = this.webAudioPeakMeter.createMeterNode(inputStreamNode, this.recorderSrvc.audioCtx)
      this.webAudioPeakMeter.createMeter(this.meterEl, this.meterNodeRaw, {})
    }

    this.recorderSrvc.startRecording()
    this.isRecording = true
    this.debugTxt.innerHTML = "запись..."
  }

  _stopAllRecording () {
    if (this.recorderSrvc && this.isRecording) {

      this.recorderSrvc.stopRecording()
      this.isRecording = false

      if (this.meterNodeRaw) {
        this.meterNodeRaw.disconnect()
        this.meterNodeRaw = null
        this.meterEl.innerHTML = ''
      }
    }
  }


  _onNewRecording (evt) {
    if (!this.saveNextRecording) {
      return
    }
    const newIdx = this.recordingsCont.childNodes.length + 1

    const newEl = document.createElement('div')
    newEl.innerHTML = '<audio id="audio-recording-' + newIdx + '" controls></audio>'
    this.recordingsCont.appendChild(newEl)

    const recordingEl = document.getElementById("audio-recording-" + newIdx);
    recordingEl.src = evt.detail.recording.blobUrl
    console.log("mimetype",evt.detail.recording.mimeType)
    console.log("blobUrl", evt.detail.recording.blobUrl)
    console.log("blobsize", evt.detail.recording.size)
    const reader = new FileReader();
    
    console.log("data raw ", evt.detail.recording.blob)
    reader.readAsArrayBuffer(evt.detail.recording.blob)
    reader.onloadend = (event) => {
    // The contents of the BLOB are in reader.result:
      //console.log("data", reader.result);
      
      // pack blob and uid data to FormData
      var formData= new FormData();
      formData.append('audio', evt.detail.recording.blob, 'blob');
      formData.append('uid', uid_);

          $.ajax(url, {
          data : formData,
          //contentType : 'audio/webm;codecs=opus',
          contentType : false,
          processData: false,
          type : 'POST',
          success: function (data) {
            console.log("success");
            },
          error: function() {
            console.log("failed");
          }
              
        });

    }

    recordingEl.type = evt.detail.recording.mimeType
  }
}

var SpeechRecognition = window.webkitSpeechRecognition;

var recognition = new SpeechRecognition();
let saveHandle

var Textbox = $("#textarea");
var instructions = $("#instructions");

var Content = "";

recognition.continuous = true;

recognition.onresult = function (event) {
    var current = event.resultIndex;

    var transcript = event.results[current][0].transcript;

    Content += transcript;
    Textbox.val(Content);
};

$("#start").on("click", function (e) {
    if ($(this).text() == "Stop Recording") {
        $(this).html("Start Recording");
        $("#instructions").html("");
        recognition.stop();
    } else {
        $(this).html("Stop Recording");
        $("#instructions").html("Recording...");
        if (Content.length) {
            Content += " ";
        }
        recognition.start();
    }
});

$("#saveas").click(function (e) {
    saveText(Content);
});

async function saveText(content) {
    const opts = {
        type: "save-file",
        accepts: [{
            description: "Text file",
            extensions: ["txt"],
            mimeTypes: ["text/plain"],
        }, ],
    };
    const handle = await window.chooseFileSystemEntries(opts);

    const writable = await handle.createWritable();
    // Write contents of file to stream
    await writable.write(content);
    // Close file and write contents to disk
    await writable.close();
}

$("#load").click(function () {
    if ($(this).html() == "Modify Changes") {
        saveFile(saveHandle, Content)
    } else {
        $(this).html("Modify Changes")
        loadFile();
    }
});
async function getNewFileHandle() {

    const handle = await window.chooseFileSystemEntries();
    return handle;
}
async function loadFile() {

    saveHandle = await getNewFileHandle()

    if (await verifyPermission(saveHandle, true)) {

        // Request permission, if user grants permission, return true
        const file = await saveHandle.getFile();
        const contents = await file.text();
        console.log(contents);
        Content += contents;
        $("textarea").val(contents);
    }
}

async function saveFile(saveHandle, content) {
    const writable = await saveHandle.createWritable();
    // Write contents of file to the stream
    await writable.write(content);
    // Close file and write contents to disk
    await writable.close();

    alert("File Changes were Saved")
}

async function verifyPermission(fileHandle, withWrite) {
    const opts = {};
    if (withWrite) {
        opts.writable = true;
    }
    // Check if we already have permission, if so, return true
    if (await fileHandle.queryPermission(opts) === 'granted') {
        return true;
    }
    // Request permission to file, if user grants permission, return true.
    if (await fileHandle.requestPermission(opts) === 'granted') {
        return true;
    }
    // User did not grant permission, return false.
    return false;
}

$("#clear").click(function () {
    Textbox.val("");
    $("#load").html("Load File")
    Content = ""
    $("#start").html("Start Recording")
});

Textbox.on("input", function () {
    Content = $(this).val();
});
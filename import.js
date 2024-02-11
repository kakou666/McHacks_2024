function importFile() {
    var fileInput = document.getElementById('fileInput');
    var textArea = document.querySelector('.textArea');
    var fileNameDisplay = document.getElementById('fileName');

    fileInput.click();

    fileInput.addEventListener('change', function () {
        var file = this.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function (e) {
                fileContent=e.target.result;
                textArea.value = fileContent;
                // fileNameDisplay.innerText = 'File: ' + file.name;
            };

            reader.readAsText(file);
        }
    });
}
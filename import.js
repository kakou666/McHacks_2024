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
                textArea.value = e.target.result; // Update to use textArea
                fileNameDisplay.innerText = 'File: ' + file.name;
            };

            reader.readAsText(file);
        }
    });
}
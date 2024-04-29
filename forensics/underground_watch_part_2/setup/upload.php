<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $target_dir = "uploads/";

    $target_file = $target_dir . basename($_FILES["file"]["name"]);

    // $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {
        echo "Your file has been successfully uploaded at ". htmlspecialchars($target_file);
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}


?>
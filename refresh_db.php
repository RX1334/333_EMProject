<?php
$servername = "energymonitor.princeton.edu";
$username = "labenerg_wolson";
$password = "lab_energy_monitoring_cos333";
$dbname = "labenerg_EMDatabase";

// Connect, check connection
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// # pull daily total
// $sql_pull = "SELECT SUM(energy_consumption) AS value_sum FROM today_fhinfo";
// $result = $conn->query($sql_pull); 
// $row = mysqli_fetch_assoc($result); 
// $daily_energy_sum = $row['value_sum'];
// echo $daily_energy_sum;

# wipe today fh table
$sql_wipe1 = "UPDATE today_fhinfo SET energy_consumption = 0";
$sql_wipe2 = "UPDATE today_fhinfo SET hours_open = 0";
# wipe today lab table
$sql_wipe3 = "UPDATE today_labinfo SET fh_consumption = 0";
$sql_wipe4 = "UPDATE today_labinfo SET climate_consumption = 0";
$sql_wipe5 = "UPDATE today_labinfo SET total_consumption = 0";
$conn->query($sql_wipe1); 
$conn->query($sql_wipe2);
$conn->query($sql_wipe3);
$conn->query($sql_wipe4);
$conn->query($sql_wipe5);

#push daily total
// $stmt = $conn->prepare("INSERT INTO daily_fhinfo (id, fh_id, lab_id, day, energy_consumption, hours_open) VALUES (?, ?, ?, ?, ?)");
// $stmt->bind_param("sss", $firstname, $lastname, $email);

// $sql_pull = "SELECT SUM(energy_consumption) AS value_sum FROM today_fhinfo";
// $result = $conn->query($sql_pull); 
// $row = mysqli_fetch_assoc($result); 
// $sum = $row['value_sum'];
// $result = $conn->query($sql);

// if ($result->num_rows > 0) {
//   // output data of each row
//   while($row = $result->fetch_assoc()) {
//     $sum += $row["hours_open"];
//   }
// } else {
//   echo "0 results";
// }
// echo $sum;
// # send status
// if ($conn->query($sql) === TRUE) {
//   echo "CRON Job executed successfully.";
// } else {
//   echo "Error" . $conn->error;
// }

$conn->close();
?>

// Specify Region
provider "aws" {
  region = "ap-southeast-2"
}

// Specify Launch Template
resource "aws_instance" "app_server" {

  launch_template {
    id      = "lt-0f6f9b389d5c00133"
    version = "$Latest"
  }


  // Tags to apply to assessment can modify if you want
  tags = {
    qut-username  = "n11963131@qut.edu.au"
    qut-username2 = "n11811749@qut.edu.au"
    purpose       = "assessment 2"
    Name          = "Group11_Terraform_test"
  }
}


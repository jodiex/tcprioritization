
sudo docker build -t qa-dashboard-db .

sudo docker container stop qa-dashboard-container
sudo docker container rm qa-dashboard-container
sudo docker run -d --name qa-dashboard-container -p 5432:5432  qa-dashboard-db


echo ""
echo ""
echo "################################"
echo "Database Created... "
echo "Please Run: "
echo "source ./env/bin/activate"
echo "python src/main.py db upgrade"
echo "################################"

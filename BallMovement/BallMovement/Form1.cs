using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
namespace BallMovement
{
    public partial class Form1 : Form
    {
        private TcpClient client;
        private NetworkStream stream;
        // Ball properties
        private int ballX = 100; // Initial X position
        private int ballY = 100; // Initial Y position
        private int ballRadius = 20; // Ball radius
        private int ballSpeed = 5; // Speed of ball movement


        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            try
            {
                client = new TcpClient();
                client.Connect(IPAddress.Parse("127.0.0.1"), 8000); // Use the same IP and port as in the Python server code
                Console.WriteLine("Connected to the server.");

                stream = client.GetStream();

                // Start listening for data in a separate thread
                Thread receiveThread = new Thread(StartListeningForCoordinates);
                receiveThread.Start();

            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message);
            }
        }

        private void StartListeningForCoordinates()
        {
            byte[] buffer = new byte[1024];
            int bytesRead;

            while (true)
            {
                try
                {
                    bytesRead = stream.Read(buffer, 0, buffer.Length);
                    if (bytesRead > 0)
                    {
                        string coordinates = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                        DisplayCoordinates(coordinates);
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error: " + e.Message);
                    break;
                }
            }

            // Clean up resources
            stream.Close();
            client.Close();
        }

        private void DisplayCoordinates(string coordinates)
        {
            if (coordinates != null)
            {
                // Split the received coordinates into left and right hand parts
                string[] handCoordinates = coordinates.Split('\n');

                if (handCoordinates.Length >= 1)
                {
                    string leftHandCoordinates = handCoordinates[0];
                    string[] leftHandParts = leftHandCoordinates.Split(',');

                    if (leftHandParts.Length >= 8) // Assuming the 4th point (thumb) is available
                    {
                        int thumbX = int.Parse(leftHandParts[6]); // Replace '6' with the correct index
                        int thumbY = int.Parse(leftHandParts[7]); // Replace '7' with the correct index

                        // Calculate new ball position based on thumb coordinates
                        ballX = thumbX;
                        ballY = thumbY;

                        // Redraw the ball
                        this.Invalidate();
                    }
                }
            }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);

            // Draw the ball at the new position
            e.Graphics.FillEllipse(Brushes.Red, ballX - ballRadius, ballY - ballRadius, 2 * ballRadius, 2 * ballRadius);
        }

    }
}
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
            if (CoordinatesTextB.InvokeRequired)
            {
                CoordinatesTextB.Invoke(new Action(() => DisplayCoordinates(coordinates)));
            }
            else
            {
                // Append the received coordinates to the existing text in the TextBox
                CoordinatesTextB.AppendText(coordinates + Environment.NewLine);
            }
        }
    }
}
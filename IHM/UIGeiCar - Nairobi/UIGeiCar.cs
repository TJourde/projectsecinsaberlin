using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;

namespace UIGeiCar___Berlin
{
    public partial class UIGeiCar : Form
    {
        TcpClient clientSocket = new TcpClient();
        NetworkStream nwStream;
        Boolean bConnected = false;
        Boolean platooning_mode = false; //hooking 
        Boolean waiting_mode = false;
        Boolean cars_connected = false;
        //Boolean 

        public UIGeiCar()
        {
            InitializeComponent();
            pictureBox3.Visible = false;
            connected.Image = Properties.Resources.led_rouge;
            BHooking.Enabled = false;
            BTowing.Enabled = false;
        }

        private void Bconnect_Click(object sender, EventArgs e)
        {
            try
            {
                clientSocket.Connect(ip.Text, 6666);
                bconnect.Text = "Connected";
                bconnect.Enabled = false;
                nwStream = clientSocket.GetStream();
                bConnected = true;
                EnableAll();
                ip.Enabled = false;
                Receive();
            }
            catch (SocketException ex)
            {
                bConnected = false;
                bconnect.Text = "Failed to connect";
                Console.WriteLine(ex.Message);
            }
        }

        private void EnableAll()
        {
            bforward.Enabled = true;
            bright.Enabled = true;
            SpdBar.Enabled = true;
            bleft.Enabled = true;
            bbackward.Enabled = true;
            bstopMOV.Enabled = true;
            bstopSTE.Enabled = true;
            //towing.Enable = true; 
        }

        private void DisableAll()
        {
            bforward.Enabled = false;
            bright.Enabled = false;
            SpdBar.Enabled = false;
            bleft.Enabled = false;
            bbackward.Enabled = false;
            bstopMOV.Enabled = false;
            bstopSTE.Enabled = false;
            //towing.Enable = false;
        }

        async void Receive()
        {

            int cmpt = 0;
            int Mask_URC = 1;
            int Mask_UFC_slave = 2;
            int Mask_MAG = 4;
            if (bConnected)
            {
                while (clientSocket.Connected)
                {
                    byte[] myReadBuffer = new byte[2048];
                    await nwStream.ReadAsync(myReadBuffer, 0, myReadBuffer.Length);
                    String st = Encoding.UTF8.GetString(myReadBuffer);
                    String[] msgs = st.Split(';');

                    foreach (String msg in msgs)
                    {
                        Console.WriteLine(msg);
                        String[] elt = msg.Split(':');
                        switch (elt[0])
                        {
                            // error msgs on the screen
                            case "ERR":
                                //Display_label_off();
                                if (Mask_MAG == (Mask_MAG & int.Parse(elt[1])))
                                { 
                                    //eWARNING_obstacle.Visible = true;
                                    mag_imm.Image = Properties.Resources.led_rouge;
                                   // Info_error.Text = "Error code: Magnetic Fail";
                                }
                                if (Mask_URC == (Mask_URC & int.Parse(elt[1])))
                                {
                                    front_imm.Image = Properties.Resources.led_rouge;
                                   // Info_error.Text = "Error code: US slave Fail";
                                }
                                if (Mask_UFC_slave == (Mask_UFC_slave & int.Parse(elt[1])))
                                {
                                    back_imm.Image = Properties.Resources.led_rouge;
                                   // Info_error.Text = "Error code: US master Fail";
                                }
                                if ((Mask_MAG == (Mask_MAG & int.Parse(elt[1]))) && (Mask_URC == (Mask_URC & int.Parse(elt[1]))) && (Mask_UFC_slave == (Mask_UFC_slave & int.Parse(elt[1]))))
                                {
                                    pictureBox3.Image = Properties.Resources.barre_no;
                                 
                                }
                                else
                                {
                                    pictureBox3.Image = Properties.Resources.barre_what;
                                }
                                break;
                            case "TOWSTATE":
                                BTowing.BackgroundImage = Properties.Resources.ON;
                                pictureBox3.Visible = true;
                                break;
                            case "MAG":
                                mag_value.Text = elt[1];
                                break;
                            case "UFC":
                                bFront.Text = elt[1];
                                break;
                            case "UFC_slave":
                                eUSFC.Text = elt[1];
                                break;
                            case "URC":
                                eUSRC.Text = elt[1];
                                break;
                            case "BAT":
                                eBAT.Text = elt[1];
                                break;
                            case "CON_PINK":
                                if (elt[1] == "on")
                                {
                                    connected.Image = Properties.Resources.led_vert;
                                    cars_connected = true;
                                    BHooking.Enabled = true;
                                    BCarsConnection.BackgroundImage = Properties.Resources.ON;
                        
                                }
                                else if (elt[1] == "off")
                                {
                                    connected.Image = Properties.Resources.led_rouge;
                                    cars_connected = false;
                                    BHooking.Enabled = false;
                                    BCarsConnection.BackgroundImage = Properties.Resources.OFF;
                                }
                                break;
                            case "STATE":
                                if(elt[1] == "approching")
                                {
                                    BHooking.BackgroundImage = Properties.Resources.wait;
                                }
                                if (elt[1]=="hooking_effective")
                                {
                                    BHooking.BackgroundImage = Properties.Resources.ON;
                                    BTowing.Enabled = true;
                                    mag_imm.Image = Properties.Resources.led_vert;
                                    front_imm.Image = Properties.Resources.led_vert;
                                    back_imm.Image = Properties.Resources.led_vert;
                                    danger.Image = null; 
                                }
                                else if(elt[1] == "hooking_uneffective")
                                {
                                    danger.Image = Properties.Resources.attention;
                                }
                                if(elt[1] == "towing_error")
                                {
                                    BTowing.BackgroundImage = Properties.Resources.OFF;
                                }
                                break;                                  
                            default:
                                cmpt = (cmpt + 1) % 100;
                                break;
                        }
                    }
                }
            }
        }

        private void Bright_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "right;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void Bbackward_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV:" + "backward;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void Bleft_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "left;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void Bforward_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV:" + "forward;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void BstopSTE_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "stop;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void BstopMOV_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV:" + "stop;");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void UIGeiCar_KeyDown(object sender, KeyEventArgs e)
        {
            byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "stop;");
            if (bConnected)
            {
                switch (e.KeyCode)
                {
                    case Keys.Down:
                        bytes = Encoding.ASCII.GetBytes("MOV:" + "backward;");
                        break;
                    case Keys.Up:
                        bytes = Encoding.ASCII.GetBytes("MOV:" + "forward;");
                        break;
                    case Keys.Left:
                        bytes = Encoding.ASCII.GetBytes("STE:" + "left;");
                        break;
                    case Keys.Right:
                        bytes = Encoding.ASCII.GetBytes("STE:" + "right;");
                        break;
                }
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void UIGeiCar_KeyUp(object sender, KeyEventArgs e)
        {
            byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "stop;");
            if (bConnected)
            {
                switch (e.KeyCode)
                {
                    case Keys.Down:
                    case Keys.Up:
                        bytes = Encoding.ASCII.GetBytes("MOV:" + "stop;");
                        break;
                    case Keys.Left:
                    case Keys.Right:
                        bytes = Encoding.ASCII.GetBytes("STE:" + "stop;");
                        break;
                }
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void UIGeiCar_FormClosing(object sender, FormClosingEventArgs e)
        {
            Application.Exit();
        }

        private void SpdBar_ValueChanged(object sender, EventArgs e)
        {
            byte[] bytes = Encoding.ASCII.GetBytes("SPE:" + SpdBar.Value.ToString() + ";");
            nwStream.Write(bytes, 0, bytes.Length);
            eSPD.Text = SpdBar.Value.ToString();
        }

        private void KbCtrl_PreviewKeyDown(object sender, PreviewKeyDownEventArgs e)
        {
            byte[] bytes = Encoding.ASCII.GetBytes("STE:" + "stop;");
            if (bConnected)
            {
                switch (e.KeyCode)
                {
                    case Keys.Down:
                        bytes = Encoding.ASCII.GetBytes("MOV:" + "backward;");
                        break;
                    case Keys.Up:
                        bytes = Encoding.ASCII.GetBytes("MOV:" + "forward;");
                        break;
                    case Keys.Left:
                        bytes = Encoding.ASCII.GetBytes("STE:" + "left;");
                        break;
                    case Keys.Right:
                        bytes = Encoding.ASCII.GetBytes("STE:" + "right;");
                        break;
                }
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void BHooking_Click(object sender, EventArgs e) //BHooking -> start_hooking 
        {
            if (bConnected) 
            {

                if (platooning_mode == false && waiting_mode == false)
                {
                    /* byte[] bytes = Encoding.ASCII.GetBytes("HOO:" + "on;"); // PLA = HOO
                     BHooking.Image = Properties.Resources.wait;
                     nwStream.Write(bytes, 0, bytes.Length);
                     platooning_mode = false;
                     waiting_mode = true;*/
                    
                    byte[] bytes = Encoding.ASCII.GetBytes("HOO:" + "start;");
                    BHooking.BackgroundImage = Properties.Resources.wait;
                    nwStream.Write(bytes, 0, bytes.Length);
                    platooning_mode = false;
                    waiting_mode = true;
                    BTowing.Enabled = true;

                }
                else
                {
                    if (platooning_mode == true || waiting_mode == true)
                    {
                        byte[] bytes = Encoding.ASCII.GetBytes("HOO:" + "stop;");
                        BHooking.BackgroundImage = Properties.Resources.OFF;
                        nwStream.Write(bytes, 0, bytes.Length);
                        platooning_mode = false;
                        waiting_mode = false;
                        //Display_label_off();
                    }
                }

            }
        }

        private void Bdisconnect_Click(object sender, EventArgs e)
        {
            try
            {
                clientSocket.Close();
                bconnect.Enabled = true;
                bdisconnect.Enabled = false;
                bConnected = false;
                ip.Enabled = true;
                DisableAll();
            }
            catch (SocketException ex)
            {
                bConnected = true;
                bconnect.Text = "Failed to disconnect";
                Console.WriteLine(ex.Message);
            }
        }

      /*  private void BPlat_accept_Click(object sender, EventArgs e)
        {
            if (waiting_mode == true)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("PLA:" + "yes;");
                BHooking.Image = Properties.Resources.ON;
                nwStream.Write(bytes, 0, bytes.Length);
                waiting_mode = false;
                platooning_mode = true;
                /*ILIDAR.Visible = true;
                eLIDAR.Visible = true;
                car_detected.Visible = false;
                BPlat_accept.Enabled = false;
                BPlat_refuse.Enabled = false;
                BPlat_accept.Visible = false;
                BPlat_refuse.Visible = false;
            }
        }

        private void BPlat_refuse_Click(object sender, EventArgs e)
        {
            if (waiting_mode == true)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("PLA:" + "no;");
                BHooking.Image = Properties.Resources.wait;
                nwStream.Write(bytes, 0, bytes.Length);
                waiting_mode = true;
                platooning_mode = false;
                /*ILIDAR.Visible = true;
                eLIDAR.Visible = true;
                car_detected.Visible = false;
                BPlat_refuse.Enabled = true;
                BPlat_accept.Visible = true;
                BPlat_refuse.Visible = true;
            }
        }*/

      /*  private void Display_label_on()
        {
            /*ILIDAR.Visible = true;
            eLIDAR.Visible = true;
            car_detected.Visible = true;
            BPlat_accept.Enabled = true;
            BPlat_refuse.Enabled = true;
            BPlat_accept.Visible = true;
            BPlat_refuse.Visible = true;
        }

        private void Display_label_off()
        {
            /*ILIDAR.Visible = false;
            eLIDAR.Visible = false;
            car_detected.Visible = false;
            BPlat_accept.Enabled = false;
            BPlat_refuse.Enabled = false;
            BPlat_accept.Visible = false;
            BPlat_refuse.Visible = false;
        }*/

        private void Lost_car_process()
        {
            byte[] bytes = Encoding.ASCII.GetBytes("PLA:" + "off;");
            BHooking.BackgroundImage = Properties.Resources.OFF;
            nwStream.Write(bytes, 0, bytes.Length);
            platooning_mode = false;
            waiting_mode = false;
        }

        //private void Start_hook_Click(object sender, EventArgs e) // private void Towing_Click(object sender, EventArgs e)
        private void Towing_Click(object sender, EventArgs e)
        {
            if (bConnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("TOW:" + "start;"); 
                BTowing.BackgroundImage = Properties.Resources.ON;
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        private void bCarsConnection_Click(object sender, EventArgs e)
        {
            if (cars_connected == false)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("CON:" + "start;");
                BCarsConnection.BackgroundImage = Properties.Resources.wait;
                nwStream.Write(bytes, 0, bytes.Length);
            }
            else
            {
                byte[] bytes = Encoding.ASCII.GetBytes("CON:" + "stop;");
                BCarsConnection.BackgroundImage = Properties.Resources.wait;
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }
        

        /* private void Info_error_Click(object sender, EventArgs e)
         {

         }

           private void IUSLC_Click(object sender, EventArgs e) //?? US sensor of the 2 car 
           {

           }

           private void InfoLayout_Paint(object sender, PaintEventArgs e)
           {

           }

           private void UIGeiCar_Load(object sender, EventArgs e)
           {

           } */
    }
}

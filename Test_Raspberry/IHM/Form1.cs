using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        public int hook_ok;
        public decimal type_error;
        public Form1()
        {
            InitializeComponent();
            start_towing.Visible = false;
            towing.Visible = false;
            hook_ok = 0;
            button1.Visible = false;
            error_message.Visible = false;
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            timertow.Start();
        }

        private void start_Click(object sender, EventArgs e)
        {
            maneuvre.Text = "In progress";
            button1.Visible = true;
        }

        private void start_towing_Click(object sender, EventArgs e)
        {
            towing.Text = "towing";
        }

        private void timertow_Tick(object sender, EventArgs e)
        {
            if (hook_ok==1)
            {
                start_towing.Visible = true;
                towing.Visible = true;
                error_message.Visible = true;
            }
            type_error = choose_error.Value;
            if (type_error == 0)
            {
                error_message.Text = "towing OK";
            }
            else if (type_error==1)
            {
                error_message.Text = "Error magnetic sensor";
            }
            else if (type_error==2)
            {
                error_message.Text = "Error US sensor";
            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            hook_ok = 1;
            maneuvre.Text = "hooked";
        }

        private void stoptow_Click(object sender, EventArgs e)
        {
            towing.Text = "Towing stoped";
        }
    }
}

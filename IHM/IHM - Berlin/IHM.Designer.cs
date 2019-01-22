namespace IHM___Berlin
{
    partial class IHM
    {
        /// <summary>
        /// Variable nécessaire au concepteur.
        /// </summary>
        private System.ComponentModel.IContainer components = null;


        /// <summary>
        /// Nettoyage des ressources utilisées.
        /// </summary>
        /// <param name="disposing">true si les ressources managées doivent être supprimées ; sinon, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Code généré par le Concepteur Windows Form

        /// <summary>
        /// Méthode requise pour la prise en charge du concepteur - ne modifiez pas
        /// le contenu de cette méthode avec l'éditeur de code.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(IHM));
            this.lblSpeed = new System.Windows.Forms.Label();
            this.lBAT = new System.Windows.Forms.Label();
            this.lUSLC = new System.Windows.Forms.Label();
            this.lUSRC = new System.Windows.Forms.Label();
            this.bconnect = new System.Windows.Forms.Button();
            this.ip = new System.Windows.Forms.TextBox();
            this.SpdBar = new System.Windows.Forms.TrackBar();
            this.bforward = new System.Windows.Forms.Button();
            this.bright = new System.Windows.Forms.Button();
            this.bleft = new System.Windows.Forms.Button();
            this.bbackward = new System.Windows.Forms.Button();
            this.bstopSTE = new System.Windows.Forms.Button();
            this.bstopMOV = new System.Windows.Forms.Button();
            this.eBAT = new System.Windows.Forms.Label();
            this.infoLayout = new System.Windows.Forms.Panel();
            this.label5 = new System.Windows.Forms.Label();
            this.bFront = new System.Windows.Forms.Label();
            this.danger = new System.Windows.Forms.PictureBox();
            this.connected = new System.Windows.Forms.PictureBox();
            this.mag_value = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.pictureBox3 = new System.Windows.Forms.PictureBox();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.eUSFC = new System.Windows.Forms.Label();
            this.eUSRC = new System.Windows.Forms.Label();
            this.eSPD = new System.Windows.Forms.Label();
            this.kbCtrl = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.bdisconnect = new System.Windows.Forms.Button();
            this.magnetic = new System.Windows.Forms.Label();
            this.frontUS = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.labelConnect = new System.Windows.Forms.Label();
            this.BCarsConnection = new System.Windows.Forms.Button();
            this.BTowing = new System.Windows.Forms.Button();
            this.back_imm = new System.Windows.Forms.PictureBox();
            this.front_imm = new System.Windows.Forms.PictureBox();
            this.mag_imm = new System.Windows.Forms.PictureBox();
            this.BHooking = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.SpdBar)).BeginInit();
            this.infoLayout.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.danger)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.connected)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.back_imm)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.front_imm)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.mag_imm)).BeginInit();
            this.SuspendLayout();
            // 
            // lblSpeed
            // 
            this.lblSpeed.AutoSize = true;
            this.lblSpeed.Location = new System.Drawing.Point(429, 28);
            this.lblSpeed.Name = "lblSpeed";
            this.lblSpeed.Size = new System.Drawing.Size(38, 13);
            this.lblSpeed.TabIndex = 9;
            this.lblSpeed.Text = "Speed";
            // 
            // lBAT
            // 
            this.lBAT.AutoSize = true;
            this.lBAT.Location = new System.Drawing.Point(3, 8);
            this.lBAT.Name = "lBAT";
            this.lBAT.Size = new System.Drawing.Size(28, 13);
            this.lBAT.TabIndex = 10;
            this.lBAT.Text = "BAT";
            // 
            // lUSLC
            // 
            this.lUSLC.AutoSize = true;
            this.lUSLC.Location = new System.Drawing.Point(160, 27);
            this.lUSLC.Name = "lUSLC";
            this.lUSLC.Size = new System.Drawing.Size(46, 13);
            this.lUSLC.TabIndex = 24;
            this.lUSLC.Text = "front US";
            // 
            // lUSRC
            // 
            this.lUSRC.AutoSize = true;
            this.lUSRC.Location = new System.Drawing.Point(13, 153);
            this.lUSRC.Name = "lUSRC";
            this.lUSRC.Size = new System.Drawing.Size(49, 13);
            this.lUSRC.TabIndex = 30;
            this.lUSRC.Text = "back US";
            // 
            // bconnect
            // 
            this.bconnect.Location = new System.Drawing.Point(196, 11);
            this.bconnect.Name = "bconnect";
            this.bconnect.Size = new System.Drawing.Size(75, 23);
            this.bconnect.TabIndex = 0;
            this.bconnect.Text = "Connect";
            this.bconnect.UseVisualStyleBackColor = true;
            this.bconnect.Click += new System.EventHandler(this.Bconnect_Click);
            // 
            // ip
            // 
            this.ip.Location = new System.Drawing.Point(13, 13);
            this.ip.Name = "ip";
            this.ip.Size = new System.Drawing.Size(177, 20);
            this.ip.TabIndex = 1;
            // 
            // SpdBar
            // 
            this.SpdBar.Enabled = false;
            this.SpdBar.Location = new System.Drawing.Point(395, 44);
            this.SpdBar.Maximum = 50;
            this.SpdBar.Name = "SpdBar";
            this.SpdBar.Size = new System.Drawing.Size(104, 45);
            this.SpdBar.TabIndex = 2;
            this.SpdBar.Value = 10;
            this.SpdBar.ValueChanged += new System.EventHandler(this.SpdBar_ValueChanged);
            // 
            // bforward
            // 
            this.bforward.Enabled = false;
            this.bforward.Location = new System.Drawing.Point(406, 66);
            this.bforward.Name = "bforward";
            this.bforward.Size = new System.Drawing.Size(75, 23);
            this.bforward.TabIndex = 3;
            this.bforward.Text = "Forward";
            this.bforward.UseVisualStyleBackColor = true;
            this.bforward.Click += new System.EventHandler(this.Bforward_Click);
            // 
            // bright
            // 
            this.bright.Enabled = false;
            this.bright.Location = new System.Drawing.Point(487, 97);
            this.bright.Name = "bright";
            this.bright.Size = new System.Drawing.Size(75, 23);
            this.bright.TabIndex = 4;
            this.bright.Text = "Right";
            this.bright.UseVisualStyleBackColor = true;
            this.bright.Click += new System.EventHandler(this.Bright_Click);
            // 
            // bleft
            // 
            this.bleft.Enabled = false;
            this.bleft.Location = new System.Drawing.Point(325, 97);
            this.bleft.Name = "bleft";
            this.bleft.Size = new System.Drawing.Size(75, 23);
            this.bleft.TabIndex = 5;
            this.bleft.Text = "Left";
            this.bleft.UseVisualStyleBackColor = true;
            this.bleft.Click += new System.EventHandler(this.Bleft_Click);
            // 
            // bbackward
            // 
            this.bbackward.Enabled = false;
            this.bbackward.Location = new System.Drawing.Point(406, 97);
            this.bbackward.Name = "bbackward";
            this.bbackward.Size = new System.Drawing.Size(75, 23);
            this.bbackward.TabIndex = 6;
            this.bbackward.Text = "Backward";
            this.bbackward.UseVisualStyleBackColor = true;
            this.bbackward.Click += new System.EventHandler(this.Bbackward_Click);
            // 
            // bstopSTE
            // 
            this.bstopSTE.Enabled = false;
            this.bstopSTE.Location = new System.Drawing.Point(325, 126);
            this.bstopSTE.Name = "bstopSTE";
            this.bstopSTE.Size = new System.Drawing.Size(104, 23);
            this.bstopSTE.TabIndex = 7;
            this.bstopSTE.Text = "Stop Rot.";
            this.bstopSTE.UseVisualStyleBackColor = true;
            this.bstopSTE.Click += new System.EventHandler(this.BstopSTE_Click);
            // 
            // bstopMOV
            // 
            this.bstopMOV.Enabled = false;
            this.bstopMOV.Location = new System.Drawing.Point(458, 126);
            this.bstopMOV.Name = "bstopMOV";
            this.bstopMOV.Size = new System.Drawing.Size(104, 23);
            this.bstopMOV.TabIndex = 8;
            this.bstopMOV.Text = "Stop Mov.";
            this.bstopMOV.UseVisualStyleBackColor = true;
            this.bstopMOV.Click += new System.EventHandler(this.BstopMOV_Click);
            // 
            // eBAT
            // 
            this.eBAT.AutoSize = true;
            this.eBAT.Location = new System.Drawing.Point(37, 8);
            this.eBAT.Name = "eBAT";
            this.eBAT.Size = new System.Drawing.Size(13, 13);
            this.eBAT.TabIndex = 45;
            this.eBAT.Text = "0";
            // 
            // infoLayout
            // 
            this.infoLayout.Controls.Add(this.label5);
            this.infoLayout.Controls.Add(this.bFront);
            this.infoLayout.Controls.Add(this.danger);
            this.infoLayout.Controls.Add(this.connected);
            this.infoLayout.Controls.Add(this.mag_value);
            this.infoLayout.Controls.Add(this.label3);
            this.infoLayout.Controls.Add(this.pictureBox3);
            this.infoLayout.Controls.Add(this.pictureBox2);
            this.infoLayout.Controls.Add(this.pictureBox1);
            this.infoLayout.Controls.Add(this.lUSLC);
            this.infoLayout.Controls.Add(this.eUSFC);
            this.infoLayout.Controls.Add(this.eUSRC);
            this.infoLayout.Controls.Add(this.lUSRC);
            this.infoLayout.Controls.Add(this.lBAT);
            this.infoLayout.Controls.Add(this.eBAT);
            this.infoLayout.Location = new System.Drawing.Point(18, 44);
            this.infoLayout.Name = "infoLayout";
            this.infoLayout.Size = new System.Drawing.Size(281, 209);
            this.infoLayout.TabIndex = 58;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(3, 27);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(46, 13);
            this.label5.TabIndex = 77;
            this.label5.Text = "front US";
            // 
            // bFront
            // 
            this.bFront.AutoSize = true;
            this.bFront.Location = new System.Drawing.Point(49, 27);
            this.bFront.Name = "bFront";
            this.bFront.Size = new System.Drawing.Size(13, 13);
            this.bFront.TabIndex = 76;
            this.bFront.Text = "0";
            // 
            // danger
            // 
            this.danger.Location = new System.Drawing.Point(93, 142);
            this.danger.Name = "danger";
            this.danger.Size = new System.Drawing.Size(73, 37);
            this.danger.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.danger.TabIndex = 74;
            this.danger.TabStop = false;
            // 
            // connected
            // 
            this.connected.Image = global::IHM___Berlin.Properties.Resources.led_rouge;
            this.connected.Location = new System.Drawing.Point(203, 152);
            this.connected.Name = "connected";
            this.connected.Size = new System.Drawing.Size(30, 27);
            this.connected.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.connected.TabIndex = 73;
            this.connected.TabStop = false;
            // 
            // mag_value
            // 
            this.mag_value.AutoSize = true;
            this.mag_value.Location = new System.Drawing.Point(59, 175);
            this.mag_value.Name = "mag_value";
            this.mag_value.Size = new System.Drawing.Size(13, 13);
            this.mag_value.TabIndex = 60;
            this.mag_value.Text = "0";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(14, 172);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(28, 13);
            this.label3.TabIndex = 59;
            this.label3.Text = "Mag";
            // 
            // pictureBox3
            // 
            this.pictureBox3.Image = global::IHM___Berlin.Properties.Resources.barre_ok;
            this.pictureBox3.Location = new System.Drawing.Point(89, 69);
            this.pictureBox3.Name = "pictureBox3";
            this.pictureBox3.Size = new System.Drawing.Size(77, 41);
            this.pictureBox3.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox3.TabIndex = 58;
            this.pictureBox3.TabStop = false;
            // 
            // pictureBox2
            // 
            this.pictureBox2.Image = global::IHM___Berlin.Properties.Resources.voiture_rose_tran;
            this.pictureBox2.Location = new System.Drawing.Point(190, 49);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(54, 99);
            this.pictureBox2.TabIndex = 57;
            this.pictureBox2.TabStop = false;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(11, 49);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(54, 99);
            this.pictureBox1.TabIndex = 44;
            this.pictureBox1.TabStop = false;
            // 
            // eUSFC
            // 
            this.eUSFC.AutoSize = true;
            this.eUSFC.Location = new System.Drawing.Point(212, 27);
            this.eUSFC.Name = "eUSFC";
            this.eUSFC.Size = new System.Drawing.Size(13, 13);
            this.eUSFC.TabIndex = 56;
            this.eUSFC.Text = "0";
            // 
            // eUSRC
            // 
            this.eUSRC.AutoSize = true;
            this.eUSRC.Location = new System.Drawing.Point(59, 153);
            this.eUSRC.Name = "eUSRC";
            this.eUSRC.Size = new System.Drawing.Size(13, 13);
            this.eUSRC.TabIndex = 54;
            this.eUSRC.Text = "0";
            // 
            // eSPD
            // 
            this.eSPD.AutoSize = true;
            this.eSPD.Location = new System.Drawing.Point(473, 28);
            this.eSPD.Name = "eSPD";
            this.eSPD.Size = new System.Drawing.Size(19, 13);
            this.eSPD.TabIndex = 59;
            this.eSPD.Text = "10";
            // 
            // kbCtrl
            // 
            this.kbCtrl.Location = new System.Drawing.Point(387, 155);
            this.kbCtrl.Name = "kbCtrl";
            this.kbCtrl.Size = new System.Drawing.Size(112, 23);
            this.kbCtrl.TabIndex = 60;
            this.kbCtrl.Text = "KeyBoard Control";
            this.kbCtrl.UseVisualStyleBackColor = true;
            this.kbCtrl.KeyDown += new System.Windows.Forms.KeyEventHandler(this.UIGeiCar_KeyDown);
            this.kbCtrl.KeyUp += new System.Windows.Forms.KeyEventHandler(this.UIGeiCar_KeyUp);
            this.kbCtrl.PreviewKeyDown += new System.Windows.Forms.PreviewKeyDownEventHandler(this.KbCtrl_PreviewKeyDown);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 16.2F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(367, 257);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(104, 26);
            this.label1.TabIndex = 61;
            this.label1.Text = "Detection";
            // 
            // bdisconnect
            // 
            this.bdisconnect.BackColor = System.Drawing.SystemColors.ControlDark;
            this.bdisconnect.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.bdisconnect.FlatAppearance.BorderColor = System.Drawing.Color.White;
            this.bdisconnect.FlatAppearance.BorderSize = 0;
            this.bdisconnect.Location = new System.Drawing.Point(292, 11);
            this.bdisconnect.Name = "bdisconnect";
            this.bdisconnect.Size = new System.Drawing.Size(75, 23);
            this.bdisconnect.TabIndex = 63;
            this.bdisconnect.Text = "Disconnect";
            this.bdisconnect.UseVisualStyleBackColor = false;
            this.bdisconnect.Click += new System.EventHandler(this.Bdisconnect_Click);
            // 
            // magnetic
            // 
            this.magnetic.AutoSize = true;
            this.magnetic.Location = new System.Drawing.Point(488, 204);
            this.magnetic.Name = "magnetic";
            this.magnetic.Size = new System.Drawing.Size(85, 13);
            this.magnetic.TabIndex = 64;
            this.magnetic.Text = "Magnetic sensor";
            // 
            // frontUS
            // 
            this.frontUS.AutoSize = true;
            this.frontUS.Location = new System.Drawing.Point(506, 257);
            this.frontUS.Name = "frontUS";
            this.frontUS.Size = new System.Drawing.Size(49, 13);
            this.frontUS.TabIndex = 66;
            this.frontUS.Text = "front US ";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(504, 304);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(52, 13);
            this.label2.TabIndex = 68;
            this.label2.Text = "back US ";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 17.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.Location = new System.Drawing.Point(228, 256);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(103, 29);
            this.label4.TabIndex = 71;
            this.label4.Text = "Hooking";
            // 
            // labelConnect
            // 
            this.labelConnect.AutoSize = true;
            this.labelConnect.Font = new System.Drawing.Font("Microsoft Sans Serif", 17.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.labelConnect.Location = new System.Drawing.Point(15, 257);
            this.labelConnect.Name = "labelConnect";
            this.labelConnect.Size = new System.Drawing.Size(186, 29);
            this.labelConnect.TabIndex = 74;
            this.labelConnect.Text = "Cars connection";
            // 
            // BCarsConnection
            // 
            this.BCarsConnection.AutoSize = true;
            this.BCarsConnection.BackgroundImage = global::IHM___Berlin.Properties.Resources.OFF;
            this.BCarsConnection.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.BCarsConnection.Location = new System.Drawing.Point(61, 287);
            this.BCarsConnection.Margin = new System.Windows.Forms.Padding(2);
            this.BCarsConnection.Name = "BCarsConnection";
            this.BCarsConnection.Size = new System.Drawing.Size(73, 30);
            this.BCarsConnection.TabIndex = 73;
            this.BCarsConnection.UseVisualStyleBackColor = true;
            this.BCarsConnection.Click += new System.EventHandler(this.BCarsConnection_Click);
            // 
            // BTowing
            // 
            this.BTowing.AutoSize = true;
            this.BTowing.BackgroundImage = global::IHM___Berlin.Properties.Resources.OFF;
            this.BTowing.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.BTowing.Enabled = false;
            this.BTowing.Location = new System.Drawing.Point(372, 287);
            this.BTowing.Margin = new System.Windows.Forms.Padding(2);
            this.BTowing.Name = "BTowing";
            this.BTowing.Size = new System.Drawing.Size(73, 30);
            this.BTowing.TabIndex = 70;
            this.BTowing.UseVisualStyleBackColor = true;
            this.BTowing.Click += new System.EventHandler(this.Towing_Click);
            // 
            // back_imm
            // 
            this.back_imm.Image = global::IHM___Berlin.Properties.Resources.led_grey;
            this.back_imm.Location = new System.Drawing.Point(516, 321);
            this.back_imm.Name = "back_imm";
            this.back_imm.Size = new System.Drawing.Size(28, 28);
            this.back_imm.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.back_imm.TabIndex = 69;
            this.back_imm.TabStop = false;
            // 
            // front_imm
            // 
            this.front_imm.Image = global::IHM___Berlin.Properties.Resources.led_grey;
            this.front_imm.Location = new System.Drawing.Point(516, 273);
            this.front_imm.Name = "front_imm";
            this.front_imm.Size = new System.Drawing.Size(28, 28);
            this.front_imm.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.front_imm.TabIndex = 67;
            this.front_imm.TabStop = false;
            // 
            // mag_imm
            // 
            this.mag_imm.Image = global::IHM___Berlin.Properties.Resources.led_grey;
            this.mag_imm.Location = new System.Drawing.Point(516, 220);
            this.mag_imm.Name = "mag_imm";
            this.mag_imm.Size = new System.Drawing.Size(28, 28);
            this.mag_imm.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.mag_imm.TabIndex = 65;
            this.mag_imm.TabStop = false;
            // 
            // BHooking
            // 
            this.BHooking.AutoSize = true;
            this.BHooking.BackgroundImage = global::IHM___Berlin.Properties.Resources.OFF;
            this.BHooking.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.BHooking.Location = new System.Drawing.Point(243, 287);
            this.BHooking.Margin = new System.Windows.Forms.Padding(2);
            this.BHooking.Name = "BHooking";
            this.BHooking.Size = new System.Drawing.Size(73, 30);
            this.BHooking.TabIndex = 62;
            this.BHooking.UseVisualStyleBackColor = true;
            this.BHooking.Click += new System.EventHandler(this.BHooking_Click);
            // 
            // IHM
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(578, 353);
            this.Controls.Add(this.labelConnect);
            this.Controls.Add(this.BCarsConnection);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.BTowing);
            this.Controls.Add(this.back_imm);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.front_imm);
            this.Controls.Add(this.frontUS);
            this.Controls.Add(this.mag_imm);
            this.Controls.Add(this.magnetic);
            this.Controls.Add(this.bdisconnect);
            this.Controls.Add(this.BHooking);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.kbCtrl);
            this.Controls.Add(this.eSPD);
            this.Controls.Add(this.lblSpeed);
            this.Controls.Add(this.bstopMOV);
            this.Controls.Add(this.bstopSTE);
            this.Controls.Add(this.bbackward);
            this.Controls.Add(this.bleft);
            this.Controls.Add(this.bright);
            this.Controls.Add(this.bforward);
            this.Controls.Add(this.SpdBar);
            this.Controls.Add(this.ip);
            this.Controls.Add(this.bconnect);
            this.Controls.Add(this.infoLayout);
            this.KeyPreview = true;
            this.Name = "IHM";
            this.Text = "IHM";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.UIGeiCar_FormClosing);
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.UIGeiCar_KeyDown);
            this.KeyUp += new System.Windows.Forms.KeyEventHandler(this.UIGeiCar_KeyUp);
            ((System.ComponentModel.ISupportInitialize)(this.SpdBar)).EndInit();
            this.infoLayout.ResumeLayout(false);
            this.infoLayout.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.danger)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.connected)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox3)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.back_imm)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.front_imm)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.mag_imm)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button bconnect;
        private System.Windows.Forms.TextBox ip;
        private System.Windows.Forms.TrackBar SpdBar;
        private System.Windows.Forms.Button bforward;
        private System.Windows.Forms.Button bright;
        private System.Windows.Forms.Button bleft;
        private System.Windows.Forms.Button bbackward;
        private System.Windows.Forms.Button bstopSTE;
        private System.Windows.Forms.Button bstopMOV;
        private System.Windows.Forms.Label lblSpeed;
        private System.Windows.Forms.Label lBAT;
        private System.Windows.Forms.Label lUSLC;
        private System.Windows.Forms.Label lUSRC;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label eBAT;
        private System.Windows.Forms.Label eUSRC;
        private System.Windows.Forms.Label eUSFC;
        private System.Windows.Forms.Panel infoLayout;
        private System.Windows.Forms.Label eSPD;
        private System.Windows.Forms.Button kbCtrl;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button BHooking;
        private System.Windows.Forms.Button bdisconnect;
        private System.Windows.Forms.Label magnetic;
        private System.Windows.Forms.PictureBox mag_imm;
        private System.Windows.Forms.Label frontUS;
        private System.Windows.Forms.PictureBox front_imm;
        private System.Windows.Forms.PictureBox back_imm;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.PictureBox pictureBox2;
        private System.Windows.Forms.PictureBox pictureBox3;
        private System.Windows.Forms.Label mag_value;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button BTowing;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.PictureBox connected;
        private System.Windows.Forms.Label labelConnect;
        private System.Windows.Forms.Button BCarsConnection;
        private System.Windows.Forms.PictureBox danger;
        private System.Windows.Forms.Label bFront;
        private System.Windows.Forms.Label label5;
    }
}
namespace WindowsFormsApp2
{
    partial class Form1
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.start = new System.Windows.Forms.Button();
            this.maneuvre = new System.Windows.Forms.TextBox();
            this.start_towing = new System.Windows.Forms.Button();
            this.towing = new System.Windows.Forms.TextBox();
            this.timertow = new System.Windows.Forms.Timer(this.components);
            this.button1 = new System.Windows.Forms.Button();
            this.stoptow = new System.Windows.Forms.Button();
            this.error_message = new System.Windows.Forms.TextBox();
            this.choose_error = new System.Windows.Forms.NumericUpDown();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.choose_error)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // start
            // 
            this.start.Location = new System.Drawing.Point(409, 43);
            this.start.Name = "start";
            this.start.Size = new System.Drawing.Size(156, 27);
            this.start.TabIndex = 0;
            this.start.Text = "Start maneuvre";
            this.start.UseVisualStyleBackColor = true;
            this.start.Click += new System.EventHandler(this.start_Click);
            // 
            // maneuvre
            // 
            this.maneuvre.Location = new System.Drawing.Point(409, 88);
            this.maneuvre.Name = "maneuvre";
            this.maneuvre.Size = new System.Drawing.Size(156, 20);
            this.maneuvre.TabIndex = 1;
            // 
            // start_towing
            // 
            this.start_towing.Location = new System.Drawing.Point(20, 145);
            this.start_towing.Name = "start_towing";
            this.start_towing.Size = new System.Drawing.Size(131, 24);
            this.start_towing.TabIndex = 2;
            this.start_towing.Text = "start towing";
            this.start_towing.UseVisualStyleBackColor = true;
            this.start_towing.Click += new System.EventHandler(this.start_towing_Click);
            // 
            // towing
            // 
            this.towing.Location = new System.Drawing.Point(20, 175);
            this.towing.Name = "towing";
            this.towing.Size = new System.Drawing.Size(131, 20);
            this.towing.TabIndex = 3;
            // 
            // timertow
            // 
            this.timertow.Interval = 50;
            this.timertow.Tick += new System.EventHandler(this.timertow_Tick);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(271, 43);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(99, 26);
            this.button1.TabIndex = 4;
            this.button1.Text = "hook_finished";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // stoptow
            // 
            this.stoptow.Location = new System.Drawing.Point(20, 204);
            this.stoptow.Name = "stoptow";
            this.stoptow.Size = new System.Drawing.Size(130, 22);
            this.stoptow.TabIndex = 5;
            this.stoptow.Text = "stop";
            this.stoptow.UseVisualStyleBackColor = true;
            this.stoptow.Click += new System.EventHandler(this.stoptow_Click);
            // 
            // error_message
            // 
            this.error_message.Location = new System.Drawing.Point(30, 292);
            this.error_message.Name = "error_message";
            this.error_message.Size = new System.Drawing.Size(241, 20);
            this.error_message.TabIndex = 6;
            // 
            // choose_error
            // 
            this.choose_error.Location = new System.Drawing.Point(31, 334);
            this.choose_error.Maximum = new decimal(new int[] {
            2,
            0,
            0,
            0});
            this.choose_error.Name = "choose_error";
            this.choose_error.Size = new System.Drawing.Size(120, 20);
            this.choose_error.TabIndex = 2;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(13, 3);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(194, 136);
            this.pictureBox1.TabIndex = 7;
            this.pictureBox1.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(659, 376);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.choose_error);
            this.Controls.Add(this.error_message);
            this.Controls.Add(this.stoptow);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.towing);
            this.Controls.Add(this.start_towing);
            this.Controls.Add(this.maneuvre);
            this.Controls.Add(this.start);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.choose_error)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button start;
        private System.Windows.Forms.TextBox maneuvre;
        private System.Windows.Forms.Button start_towing;
        private System.Windows.Forms.TextBox towing;
        private System.Windows.Forms.Timer timertow;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button stoptow;
        private System.Windows.Forms.TextBox error_message;
        private System.Windows.Forms.NumericUpDown choose_error;
        private System.Windows.Forms.PictureBox pictureBox1;
    }
}


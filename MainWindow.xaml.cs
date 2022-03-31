using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WhatCalendarWeek
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    /// 
    using System;
    using System.Collections;
    using System.Globalization;
    public partial class MainWindow : Window
    {
        public static int GetWeekNumber(DateTime date)
        {
            // Iso8601
            return CultureInfo.InvariantCulture.Calendar.GetWeekOfYear(date, CalendarWeekRule.FirstFourDayWeek, DayOfWeek.Monday);
        }

        public static DateTime GetWeekDate(int CW, int year)
        {
            // Iso8601
            // Point to middle (thursday) of the year's first week (FirstFourDayWeek Calendar rule), find monday of the week and increment by 7*(Weeknumber - 1)
            DateTime midWeek1 = new(year, 1, 1);
            while (midWeek1.DayOfWeek != DayOfWeek.Thursday)
                midWeek1 = midWeek1.AddDays(1);

            DateTime monday = midWeek1.AddDays(-3);

            return monday.AddDays(7 * (CW - 1));
        }

        public MainWindow()
        {
            InitializeComponent();
            tbCWText.Text = GetWeekNumber(DateTime.Today).ToString();
        }

        private void Today_Click(object sender, RoutedEventArgs e)
        {
            calDate.SelectedDate = DateTime.Today;
            calDate.DisplayDate = DateTime.Today;
        }

        private void Calendar_OnSelectedDatesChanged(object sender, SelectionChangedEventArgs args)
        {
            if(calDate.SelectedDate == null)
            {
                calDate.SelectedDate = DateTime.Today;
            }
            DateTime dateSelected = calDate.SelectedDate.Value;
            tbCWText.Text = GetWeekNumber(dateSelected).ToString();
        }

        private void TextBox_OntextChanged(object sender, TextChangedEventArgs args)
        {
            int cWeek = Int32.Parse(tbCWText.Text);
            if (cWeek < 1)
                cWeek = 1;
            else if (cWeek > 52)
                cWeek = 52;
            
            // TO-DO : Call GetWeekDate() and set calendar automatically
        }

        private void CWeek_Click(object sender, RoutedEventArgs e)
        {
            int cWeek = Int32.Parse(tbCWText.Text);
            if (cWeek < 1)
                cWeek = 1;
            else if (cWeek > 52)
                cWeek = 52;
            
            calDate.SelectedDate = DateTime.Today;
            
            int cYear = calDate.SelectedDate.Value.Year;
            DateTime date = GetWeekDate(cWeek, cYear);

            calDate.SelectedDate = date;
            calDate.DisplayDate = date;
        }
    }

    // TO-DO BACKLOG:
    // 1) get rid of '^' button, handle Textbox change and set calendar date automatically
    // 2) 
}

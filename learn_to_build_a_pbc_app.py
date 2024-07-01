import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from PIL import Image

im="chart_with_upwards_trend"
st.set_page_config(
    page_title="Building a PBC",
    page_icon=im,
    initial_sidebar_state='collapsed')

st.title("Learn to build a Process Behavior Chart")
#st.markdown("### By Jim Lehner")

# read_csv from github repo
#dataset_url = "https://raw.githubusercontent.com/jimlehner/datasets/main/sales_data.csv"
# dataset_url = "https://raw.githubusercontent.com/jimlehner/datasets/main/How_to_build_a_PBC_Manufacturing%20Data.csv"
dataset_url = "https://raw.githubusercontent.com/jimlehner/datasets/main/learn_to_build_a_pbc_manufacturing_data.csv"
worksheet_url = "https://github.com/jimlehner/datasets/blob/2513d674c4029c9616082f4a4b6e924802ac588a/How_to_build_a_PBC_worksheet_childhood_poverty_data.xlsx"

# Read csv from URL
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url, index_col=0)

# Get data 
df = get_data()

# Create dataframe that includes moving range values
mR_df = df.copy()
mR_df['Moving range'] = abs(df['Value'].diff())

# Create AmR_df
AmR_df = mR_df.copy()
AmR_df['AmR'] = round(mR_df['Moving range'].mean(),2)

# Create process_limit_df
process_limit_df = AmR_df.copy()

# Calculate process limits 
mean = round(df['Value'].mean(),2)
AmR = round(mR_df['Moving range'].mean(),2)
UPL = round(mean + (2.66*AmR),2)
LPL = round(mean - (2.66*AmR),2)
LPL = max(LPL, 0.00)
URL = round(3.27*AmR,2)
process_limit_df['UPL'] = [UPL]*len(df)
process_limit_df['LPL'] = [LPL]*len(df)
process_limit_df['URL'] = [URL]*len(df)

# Complete dataframe
complete_df = process_limit_df.copy()
complete_df['Mean'] = [mean]*len(df)

# Special cause dataframe
special_cause_df = complete_df[(complete_df['Value'] > UPL) |
                               (complete_df['Value'] == LPL)]

# Sidebar
with st.sidebar:
    st.markdown("# About the project")
    st.markdown(
        """
        This project is part of a larger effort to increase the understanding and use of Process Behavior Charts, otherwise known as control charts, in manufacturing specifically and business in general.
         
        """)
    st.markdown(" # About the creator")
    st.markdown(
        """
        Jim Lehner is a mechanical engineer working in manufacturing. His interests rest at 
        the confluence of industry and data science. He has worked in aerospace, industrial machining, automotive, and healthcare. 
        
        For collaborations contact Jim via email or linkedin:
        """
    )
    st.markdown(
        """
        James.Lehner@Gmail.com

        """
    )
    st.markdown(
        """
        https://www.linkedin.com/in/jim-lehner/
        """
    )
    
    #st.markdown("# Contact")
    #st.markdown(
    #    """
    #    To learn more about the use and application of Process Behavior Charts in industry and elsewhere contact Jim Lehner. 
    #    """
    #)
    #url = "https://www.createholisticsolutions.com/"
    #st.markdown("[link]" % url)

select_step = st.selectbox("Select a step", ['Introduction', 
                                             'Step 1: Gather the data',
                                             'Step 2: Calculate the mean',
                                             'Step 3: Calculate the moving ranges',
                                             'Step 4: Calculate the average moving range', 
                                             'Step 5: Calculate the process limits',
                                             'Step 6: Put it all together!'])#,
                                             #'Interpreting a PBC',
                                             #'Interpreting the PBC'])#,
                                             #"The Why-What-How of PBCs"])
if select_step == "Introduction":
    
    st.markdown("## A place to start")
    
    st.markdown(
        """
        **Process Behavior Charts (PBCs)**, otherwise known as control charts, are an analysis tool used for predicting how a process will behave in the future
        based on how it has behaved in the past. Such knowledge, regardless of industry or application, is quintessential to the improvement, 
        optimization, and management of processes and systems. Of course, to unlock such knowledge, relies on the capacity to build a PBC. 
        """
        )
    
    st.markdown(
        """
        Given their value, building a PBC is a task that should be common and fool proof. Unfortunately, this is not the case. More often than not PBCs
        are overlooked and ignored. Their use is relegated to expensive software and an ever expanding list of tools and techniques that promise to transform
        your organization. PBCs are seen as lacking utility due to a lack of understanding regarding why, when, and how they should be used. Whether due to neglect 
        or due to ignorance this trend cannot continue. Failure to direct time, attention, and resources to areas that need it most cannot persist.
        """
    )

    st.markdown(
        """
        Here, you will learn how to build a PBC with the tools you have at hand. Here, you will learn to turn data into insights and insights into actions by building 
        a PBC in 6 steps. These steps are:
        """
    )

    st.markdown(
        """
        1. Gather the data
        2. Calculate the mean
        3. Calculate the moving range
        4. Calculate the average moving range
        5. Calculate the process limits
        6. Put it all together!
        """
    )
    
    st.markdown(" ### The data")
    st.markdown(
        """
        To help facilitate your understanding of these steps, we will use data from an automated manufacturing process. 
        To download a copy of the dataset click the "Download data as CSV" button.
        """
    )

    col1, col2 = st.columns([2,1])
    with col1:
        #st.markdown(" ## Poverty data")
        st.dataframe(df,height=425, width=250)
    
    with col2:
        @st.cache_data
        def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation at on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='manufacturing_process_data.csv',
            mime='text/csv')

elif select_step == 'Step 1: Gather the data':
    st.markdown("## Step 1: Gather the data")
    st.markdown(
        """
        Gathering data is an often overlooked but quintessential step in building a PBC. Aside from the obvious notion that without data a PBC cannot exist,\
        the process of gathering data increases familiarity with the **Data Generating Process (DGP)**. 
        
        In statistics, a DGP is the system that produces the data \
        of interest. Depending on the industry, DGPs will take different forms and have different characteristics. In manufacturing, a DGP might be an \
        automated system that produces widgets. In education, a DGP might be the system used to educate or evaluate students. In healthcare, the DGP might be \
        the method used to evaluate patient outcomes. Regardless of the industry and regardless of the DGPs form, gathering data is an opportunity to learn more \
        about the system that produced it.
        """
    )
    
# =============================================================================
    DGP_image = Image.open(r'images\Data Generating Process - DGP_cropped.png')
# =============================================================================
    # DGP_image = Image.open('Data Generating Process - DGP_cropped.png')

    st.image(DGP_image, caption='The Data Generating Process (DGP) geneartes data \
             that creates a model used to approximate the DGP.')

    st.markdown(
        """
        Knowledge of the DGP is not the only opportunity present while gathering data. It is also an opportunity to ensure that the data being \
        collected is organized and structured in a format that is amiable to building a PBC. As we will discuss in step 6, *Put it all together!*, the foundation \
        of a PBC is the time-series. As the name suggests, time-series visualize how data changes with respect to time. While gathering data, the \
        opportunity to organize it in a PBC friendly format, one that reflects the needs of the underlying time-series, is distinctly present.
        """
    )

    st.markdown(
        """
        To this end, data should be organized such that each point can be associated with unique timestamps of equal intervals. Such a structure is reflected \
        in the manufacturing data below. Here, the timestamps of equal intervals are listed in the row labeled *Year* with the associated value listed \
        in the row labeled *Value*. The friction of performing subsequent steps, like calculating moving ranges, will be significantly reduced by \
        this intentional structuring.
        """
    )
    
    st.markdown(" ### The data")
    st.markdown(
        """
        In case you have not already done so the data we will be using and evaluating to build a PBC is below. Click the *Download data as CSV*
        button to download a copy. Once downloaded open the data in your favorite spreadsheet applicaiton (we suggest google sheets).
        """
    )
    col1, col2 = st.columns([2,1])
    with col1:
        #st.markdown(" ## Poverty data")
        st.dataframe(df)
    
    with col2:
        @st.cache_data
        def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation at on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='manufacturing_data.csv',
            mime='text/csv')


elif select_step == 'Step 2: Calculate the mean':
    st.markdown("## Step 2: Calculate the mean")

    st.markdown(
        """
        Calculating the **mean** is quintessential to the construction of PBCs. This will be made more evident when calculating process limits in step 5, *Calculate the process limits*. 
        The mean, along with average moving range and a numeric constant, are the three terms used to calculate the Upper Process Limit 
        (UPL) and Lower Process Limit (LPL). The mean will also be used as a visual reference for the data’s middle in the PBC.
        """
    )

    #st.latex(r'''
    #mean = \frac{sum-of-all-terms}{number-of-values}
    #''')
    st.markdown(
            """
            While it is unlikely that you will ever have to calculate the mean by hand, knowledge of the calculation 
            facilitates an interstitial understanding of the statistic. Hence why we will explore it here. The mean is calculated in three steps:
            """
        )

    col1, col2 = st.columns(2)
    
    with col1: 

        st.markdown(
            """
            1. Sum all of the terms in the dataset (numerator)
            2. Determine the number of values in the dataset (denominator)
            3. Divide the numerator by the denominator to calculate the mean        
            """
        )
    
    with col2:
        st.latex(r'''
        mean = \frac{sum-of-all-terms}{number-of-values}
        ''')
    
    # Calculation
    st.write(" ### Your turn")
    
    st.markdown("Download a copy of the data below by clicking *Download data as CSV*. Using your favorite \
                spreadsheet application (we suggest google sheets) determine the value associated with each \
                    of the three steps used to calculate the mean.")

    col3, col4 = st.columns([2,1])
    with col3:
        st.dataframe(df, height=250)
    with col4:
        @st.cache_data
        def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation at on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label='Download data as CSV',
            data=csv,
            file_name='manufacturing_data.csv',
            mime='text/csv')
        
    # steps for calculating the mean
    st.write(" ### 1. Sum all of the terms")
    mean_numerator = st.selectbox("What is the sum of all the values in the 'Values' column in the above table?",
                                ('-','65.6','6.65','67','66.5'))
    if mean_numerator == '65.6':
        st.write(":red[65.6 is incorrect. Try again.]")
    elif mean_numerator == '6.65':
        st.write(":red[This is close but the decimal is in the wrong place. Try again!]")
    elif mean_numerator == '67':
        st.write(":red[67 is a little high. Try your calculation one more time.]")
    elif mean_numerator == '66.5':
        st.markdown(":green[That's correct! The sum of all the values in the 'Values'\
                    column is 66.5. We will use this value as the numerator when we calculate the mean. Great work! 😄]")
   
    # step 2 for calculating the mean
    st.write(" ### 2. Determine the number of values")
    mean_denominator = st.selectbox('How many values are in the data set?',
                                ('-','0','60','59','15'))
    if mean_denominator =='0':
        st.write(":red[By definition of its existence this data set cannot have 0 values. Try again.]")
    elif mean_denominator == '59':
        st.write(":red[In Python, the initial element of a sequence is assigned the index 0. \
                    This is called zero-based numbering. While the table to the left shows 0 to 9 \
                    in the first column, there is actually more than 9 values in the data set. Try again.]")
    elif mean_denominator == '60':
        st.write(":green[That's correct! There are 10 values in the data set. When calculating the mean \
                    we will use 11 as the denominator.] 😄")
    elif mean_denominator == '15':
         st.write(":red[15 is not correct. Try again.]")
  
                
    # Step 3 calculate the mean
    st.write(" ### 3. Calculate the mean")
    st.write(
        """
        To calculate the mean divide the sum of all the values in the data set by the total number of values in the data set. 
        """
    )
    mean_calc = st.selectbox('What is the mean childhood poverty rate for 2010 to 2020?',
                                ('-','1.12','1.11','2.11','1.01'))
    if mean_calc =='1.12':
        st.write(":red[1.12 is the median not the mean. Try again!]")
    elif mean_calc == '1.11':
        st.markdown(":green[That's correct! The mean of the 'Value' column is 1.11. Great Work!] 😄")
    elif mean_calc == '2.11':
        st.write(":red[That's a little high. Check your calcualtion and try again.]")
    elif mean_calc == '1.01':
        st.write(":red[Close but no cigar. Did you miss a decimal point?]")

    st.markdown("### Check your work")
    with st.expander("Show calculation of mean"):
        st.latex(r'''
        mean = \frac{sum-of-all-terms}{number-of-values}
        ''')
        st.latex(r'''
        mean = \frac{66.5}{60}
        ''')
        st.latex(r'''
        mean = 1.11
        ''')

elif select_step == 'Step 3: Calculate the moving ranges':
    st.markdown("## Step 3: Calculate the moving ranges")

    st.markdown(
        """
        Calculating the **moving range values (mRs)** is the cursory step to calculating the average moving range (AmR). Moving range values
        are a measure of the point-to-point variation in a dataset. For the manufacturing data, the moving range values are a measure 
        of the measurment-to-measurment variation of parts. 
        
        Moving ranges are calculated by finding the absolute value of the difference between subsequent values 
        in a dataset. For instance, the first observation in the 'Value' column of the manufacturing data set is 0. while the second observation value is 0.82.
        This makes the first moving range 0.82. 
        """
    )

    # calculation of mR_1
    st.latex(r'''
        mR_1= abs(0.00 - 0.82) 
        ''')
    st.latex(r'''
        mR_1 = 0.82
        ''')

    st.markdown(
        """
        The seconnd observation value is 0.82 and the third observation value is 0.98. This makes the second moving range 0.16. 
        """
    )
    # calculation of mR_2
    st.latex(r'''
        mR_2= abs(0.82 - 0.98) 
        ''')
    st.latex(r'''
        mR_2= 0.16
        ''')

    st.markdown(
        """
        The third moving range for the manufacturing dataset is 0.09. It is the absolute value of the difference between the third observation value of 0.98 and the 
        fourth observation value of 0.89. 
        """
    )     

    # calculation of mR_3
    st.latex(r'''
        mR_3 = abs(0.98-0.89)
        ''')
    st.latex(r'''
        mR_3 = 0.09 
        ''')
    
    st.write(" ### Your turn")
    
    st.markdown(
        """
        Continue this process until you've calculated all the moving range values and answered  the questions below.
        """
    )
    #st.markdown(" ## The data")
    with st.expander("See dataframe and download data"):
        col5, col6 = st.columns([2,1])
        with col5:
            st.dataframe(df)
        with col6:
            @st.cache_data
            def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation at on every rerun
                return df.to_csv().encode('utf-8')

            csv = convert_df(df)
            st.download_button(
                label='Download data as CSV',
                data=csv,
                file_name='manufacturing_data.csv',
                mime='text/csv')
        
    st.markdown(" ### Questions")
    # Question 1
    mR_Q1 = st.selectbox('How do you calculate a moving range value?',
                         ('-','Sum all of the values in the dataset',
                          'Find the difference between subsequent values in a dataset',
                          'Sum all of the values in a data set and divide by the number of values in the dataset',
                          'Find the absolute value of the difference between subsequent values in a dataset'))
    if mR_Q1 == 'Sum all of the values in the dataset':
        st.markdown(":red[Summing all of the values in the dataset would simply be the sum of all the values in the dataset, not a moving range value. Try again.]")
    elif mR_Q1 == 'Find the difference between subsequent values in a dataset':
        st.markdown(":red[Finding the difference between subsequent values is only part of calculating a moving range value]")
    elif mR_Q1 == 'Sum all of the values in a data set and divide by the number of values in the dataset':
        st.markdown(":red[This is how you calculate the mean not a moving range value. Try again.]")
    elif mR_Q1 == 'Find the absolute value of the difference between subsequent values in a dataset.':
        st.markdown(":green[That's correct! Moving range values are calculated by finding the absolute value of the difference of subsequent values in a dataset. Great job!]")

    # Question 2
    mR_Q2 = st.selectbox('What is the fifth moving range (mR)?',
                 ('-','0.82','0.63','-0.63','0.87'))
    if mR_Q2 == '0.82':
        st.markdown(":red[0.82 is one of the moving range values but not the fifth moving range value. Try again.]")
    elif mR_Q2 == '0.63':
        st.markdown(":green[Correct! The aboslute value of the difference between the forth observation value (1.76) and the fifth observation value (1.12) is 0.63. Great work!]")
    elif mR_Q2 == '-0.63':
        st.markdown(":red[-0.63 is not correct. Remember moving range values are the absolute value of the difference between subsequent values in a dataset. Try again.]")
    elif mR_Q2 == '0.87':
        st.markdown(":red[0.87 is one of the moving range values but not the fifth moving range value. Try again.]")
    
    # Question 3
    mR_Q3 = st.selectbox('What is the tenth moving range (mR) value?',
                 ('-','-0.05','0','60','0.05'))
    if mR_Q3 == '-0.05':
        st.markdown(":red[-0.05 is not correct. Remember moving range values are the absolute value of the difference between subsequent values in a dataset. Try again.]")
    elif mR_Q3 == '0.82':
        st.markdown(":red[0.82 is the first moving range value. Try again.]")
    elif mR_Q3 == '60':
        st.markdown(":red[60 is the number of values in the dataset not one of the moving range values. Try again.]")
    elif mR_Q3 == '0.05':
        st.markdown(":green[Correct! The aboslute value of the difference between the ninth observation value (0.76) and the tenth observation value (0.81) is 0.05. Great work!]")

    st.markdown("With a complete list of moving range values in hand, the next step is to calculate the **average moving range (AmR)**.")

    # Dataframe including moving range values
    st.markdown(" ### Check your work")
    with st.expander("See dataframe with moving range values"):
        st.dataframe(mR_df)

elif select_step == 'Step 4: Calculate the average moving range':
    st.markdown("## Step 4: Calculate the average moving range")
    st.markdown(
        """
        With the moving range values in hand, calculating the **average moving range (AmR)** is trivial. The average moving range is the mean of the moving range values. As was the case 
        when calculating the mean, the average moving range is the sum of all the values in a dataset divided by the number of values in the dataset. 
        """
    )

    st.markdown(
        """
        The average moving range is calclualted in three steps:
        """
    )

    col7, col8 = st.columns(2)
    with col7:
        st.markdown(
            """
            1. Sum all of the moving range (mR) values (numerator)
            2. Determine the number of values (denominator)
            3. Divide the numerator by the denominator to calculate the average moving range (AmR)
            """
        )
    with col8:
        st.latex(r'''
        AmR = \frac{sum-of-moving-ranges}{number-of-values}
        ''')

    st.markdown(" ### 1: Sum of moving range (mR) values")
    AmR_numerator = st.selectbox("What is the sum of all the moving range values?",
                                ('-','28.55','26','25.85','2.58'))
    if AmR_numerator == '28.55':
        st.write(":red[That's not correct. Try again.]")
    elif AmR_numerator == '26':
        st.write(":red[That's not correct. Try again.]")
    elif AmR_numerator == '25.85':
        st.write(":green[Correct! The sum of all the moving range values is 25.85.]")
    elif AmR_numerator == '2.58':
        st.markdown(":red[2.58 is not correct. Try again.]")

    st.markdown(" ### 2: Determine the number of mR values")
    AmR_denominator = st.selectbox("How many moving range values are in the dataset?",
                                ('-','59','60','58','61'))
    if AmR_denominator == '59':
        st.write(":green[Correct! There are 59 moving range values in the datset.]")
    elif AmR_denominator == '58':
        st.write(":red[58 is too few moving range values. Try again.]")
    elif AmR_denominator == '60':
        st.write(":red[60 is too many moving range values. Try again.]")
    elif AmR_denominator == '61':
        st.markdown(":red[61 is too many moving range values. Try again.]")

    st.markdown(" ### 3: Calculate the average moving range (AmR)")
    AmR_denominator = st.selectbox("What is the average moving range?",
                                ('-','60','1.11','4.40','0.44'))
    if AmR_denominator == '60':
        st.write(":red[60 is the number of values in the dataset not the average moving range. Try again.]")
    elif AmR_denominator == '1.11':
        st.write(":red[1.11 is the mean not the average moving range of the dataset. Try again.]")
    elif AmR_denominator == '4.40':
        st.write(":red[4.40 is not correct. Check your arithmatic and try again.]")
    elif AmR_denominator == '0.44':
        st.markdown(":green[Correct! The average moving range for the dataset is 0.44.]")

    st.markdown(
        """
        With the mean and average moving range in hand, the next step is to 
        calculate the **process limits**. Process limits are the defining features of a PBC. They are the 
        mechanism by which we characterize a process as either predictable or unpredictable.
        """
    )
    # check your work expander 
    st.markdown(" ### Check your work")
    with st.expander("Show calculation for average moving range"):
        st.latex(r'''
        AmR = \frac{sum-of-moving-ranges}{number-of-values}
        ''')
        st.latex(r'''
        AmR = \frac{25.85}{59}
        ''')
        st.latex(r'''
        AmR = 0.44
        ''')
    with st.expander("Show dataframe"):
        st.dataframe(AmR_df)

elif select_step == 'Step 5: Calculate the process limits':
    st.markdown("## Step 5: Calculate the process limits!")
    
    st.markdown(
        """
        Acting as a boundary between variation that is to be expected (common) and variation that is out-of-the-ordinary (special), **process limits** are the defining features of PBCs. 
        While there are many types of PBCs, the PBC that is most useful and easiest to implement is the **XmR-chart**. XmR-charts, called I-MR-charts in some software, are composed of two plots, an individual 
        values plot and a moving range plot. Collectively, these plots necessitate the calculation of three process limits, the **upper process limit (UPL)**, the **lower process limit (LPL)**, and the **upper range limit (URL)**. 
        """
    )
    
    st.markdown("### Process limits for the X-chart")

    st.markdown(
        """
        For the X-chart, also called the individual values plot, the **UPL** and **LPL** must be calculated. These calculations use the mean and average moving 
        range of the data as well as a numeric constant, C1. C1 is an experimentally determined scaling factor. It is required to convert the average moving range 
        into the appropriate amount of spread for the individual values in the dataset. With respect to the manufacturing dataset, the value of C1 is 2.66. In cases where
        individual values are plotted, as opposed to subgroups, C1 will always be equal to 2.66. 
        """
    )
    
    st.latex(r'''
    UPL = mean + (C1*AmR)
    ''')

    st.latex(r'''
    LPL = mean - (C1*AmR)
    ''')

    st.markdown("#### Note")

    st.markdown(
        """
        In most instances it is unlikely that the value of the LPL will be less than zero. In such cases, when the calculated value of the 
        LPL is less than zero, the LPL should, by default, be set to zero. For instance, the values in the manufacturing dataset examined here cannot have a value less than zero.
        This is because they represent a part dimension which, by definition, cannot be negative. 
        """
    )
    
    st.markdown("### Your turn")

    st.markdown(
        """
        Given a mean 1.11 and average moving range of 0.44 calculate the UPL and LPL. 
        """
    )
    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### UPL")
        UPL_Q1 = st.selectbox('What is the upper process limit (UPL)?',
                              ('-',
                              '0.82',
                              '2.27',
                              '0.98'))
        if UPL_Q1 == '0.82':
            st.markdown(":red[0.82 is the first moving range value not the UPL. Try again.]")
        elif UPL_Q1 == '2.27':
            st.markdown(":green[Correct! The UPL is 2.27. Great work!] 😄")
        elif UPL_Q1 == '0.98':
            st.markdown(":red[0.98 is in the dataset but not the UPL. Try again.]")
    with colB:    
        st.markdown("#### LPL")
        LPL_Q1 = st.selectbox('What is the lower process limit (LPL)?',
                                ('-',
                                '1.1',
                                '-0.06',
                                '0'))
        if LPL_Q1 == '1.1':
            st.markdown(":red[1.1 is the AmR not the LPL. Try again.]")
        elif LPL_Q1 == '-0.06':
            st.markdown(":red[-0.06 is the calculated LPL however, in this instance, the LPL cannot be less than zero. This means the LPL defaults to what value?]")
        elif LPL_Q1 == '0':
            st.markdown(":green[Correct! 0 is the LPL because the value of a measured part, such is the case with the manufacturing dataset, cannot be less than zero. For this reason, the calculated value of -0.06 for the LPL defaults to zero. Great work!] 😄")
    st.markdown(" #### Check your work")
    with st.expander('Show UPL and LPL calculations and values'):
        colU, colL = st.columns(2)
        with colU:
            st.latex(r'''
            UPL = 1.11 + (2.66*0.44)
            ''')
            st.latex(r'''
            UPL = 1.11 + (1.17)
            ''')
            st.latex(r'''
            UPL = 2.27
            ''')
        with colL:
            st.latex(r'''
            LPL = 1.11 - (2.66*0.44)
            ''')
            st.latex(r'''
            LPL = 1.11 - (1.17)
            ''')
            st.latex(r'''
            LPL = max(-0.06, 0)
            ''')

            st.latex(r'''
            LPL = 0
            ''')

    st.markdown("### Process limit for the mR-chart")

    st.markdown(
        """
        Unlike the X-chart (individual values plot), only one limit is associated with the moving range plot (mR-chart). This limit is called the **upper range limit (URL)**. The URL is calculated using the average moving range and a second 
        numeric constant, C2. Like C1, C2 is an experimentally determined scaling factor. It is required to convert the average moving range into the appropriate amount of spread for the moving range plot. 
        For a moving range plot with differences calculated from subsequent values the value of C2 is 3.27. Like C1, the value of C2 will change when subgroups are used. 
        """
    )

    st.latex(r'''
    URL = C2*AmR
    ''')

    st.markdown("""#### Your turn""")    

    st.markdown(
        """
        Given an average moving range of 1.1% calculate the upper range limit (URL). Using the above formula, the URL is calculated to be 3.6%. 
        """
    )

    st.markdown(" #### URL")
    URL_Q1 = st.selectbox('What is the upper range limit?',
                                ('-',
                                '0.44',
                                '1.11',
                                '1.43'))
    if URL_Q1 == '0.44':
        st.markdown(":red[0.44 is the AmR not the URL. Try again.]")
    elif URL_Q1 == '1.11':
        st.markdown(":red[1.11 is the UPL not the URL. Try again.]")
    elif URL_Q1 == '1.43':
        st.markdown(":green[Correct! 1.43 is the URL. Great work!] 😄")
    
    st.markdown(" ### Check your work")
    with st.expander("Show URL calculation and value"):
        st.latex(r'''
        URL = 3.27*0.44
        ''')

        st.latex(r'''
        URL = 1.43
        ''')

    st.markdown(
        """
        With the **process limits** in hand we have calculated all of the necessary values used to create a PBC. The final step, 
        *Put it all together!*, will coalesce these values into a single figure creating a PBC. 
        """
    )

    # check your work expander 
    st.markdown(" ### The data")
    with st.expander("Show dataframe with process limits"):
        st.dataframe(process_limit_df)

elif select_step == 'Step 6: Put it all together!':
    st.markdown("## Step 6: Put it all together!")

    st.markdown(
        """
        With process limits calculated, it's time to coalesce the previous work into a PBC. Recall that PBCs are composed of two plots, 
        an **individual values plot (X-chart)** and a **moving range plot (mR-chart)**. Collectively, these plots form an **XmR-chart** which is another name for a PBC. 
        The first plot, the X-chart, sequentially plots the individual values contained within the dataset. The second plot, the mR-chart, plots the absolute value 
        of the difference between subsequent values in the dataset. 
        """
    )

    st.markdown("### Time series of manufacturing data")
    
    st.markdown(
        """
        The figure below shows the manufacturing data as a time series. 
        In the previous steps we calculated the mean, moving range values, average moving range, and process limits using the data shown in this time sereies. 
        Recall that the foundation of any PBC is the time-series. The mean can be toggled on and off with the checkbox. When shown, the mean is displayed as a black dotted line with a value of 1.11. This was previously calculated in step 2 and used 
        to calculate the upper and lower process limits in step 5. What conclusions, if any, can you make about the manufacturing process given this time series?
        """
    )
    # Create plotly function for plotting data with mean
    def plotly_plot(df,parameter,xtick_labels,xlabel='Observation',ylabel='Value',checkbox_arg='mean'):
        # Create checkboc to control mean 
        plot_mean = st.checkbox('Show '+checkbox_arg,value=True)
        # Specify variables
        data = df[parameter]
        xlabels = df.index.tolist()
        # Calculate basic statistics
        mean = round(data.mean(),1)
        # Create figure object and plot data
        #fig = px.line(df, x=xlabels, y=parameter,markers=True)
        fig = px.line(df, x=xlabels, y=parameter,markers=True,
                    labels={
                        'x':xlabel,
                        parameter:ylabel
                    })
        # Conditionally plot mean 
        if plot_mean:
            fig.add_hline(mean, line_dash='dash',line_color='black',
                      annotation_text='Mean: ' + str(mean))
        # Add centerline
        #fig.add_hline(mean, line_dash='dash',line_color='black',
        #              annotation_text='Mean: ' + str(mean))
        # Specify annotations 
        fig.update_annotations(font_size=18, font_color='black')
        # Show fig in plotly
        st.plotly_chart(fig,use_container_width=True)
    
    #st.markdown("### Time series of manufacturing data")
    # Show individual values plot 
    plotly_plot(df,'Value', df.index)
    #st.caption('The X-chart starts its life as a time series of the individual values contained within the data set.')
    
    st.markdown("### Time series of moving range values")
    
    st.markdown(
        """
        The second plot, the moving range plot (mR-chart), sequentially plots the moving range values calculated in step 3.
        Recall that the moving range values are the absolute value of the difference between subsequent values in a data set. The average moving 
        range, shown as a black dotted line, is the average of the moving range values. This was previously calculated in step 4. Technically, the time 
        series of average moving range values is a derived time series, as opposed to just a time series. This is because the values shown in the plot are
        only made avalible for use through calculation. 
        """
    )
    #st.markdown("### Time series of moving range values")
    # Create checkbox to control average moving range 
    plot_AmR = st.checkbox('Show Average Moving Range (AmR)',value=True)

    # Specify variables for mR-plot
    data = mR_df['Moving range']
    xlabels = df.index.tolist()
    # Calculate basic statistics
    AmR = round(data.mean(),1) # In this case calculate average moving range
    # Create figure object and plot moving range values
    #fig = px.line(df, x=xlabels, y=parameter,markers=True)
    fig = px.line(df,x=xlabels,y=data,markers=True,
                labels={
                    'x':'Observation',
                    'y':'Moving Range'
                })
    # Conditionally plot average moving range 
    if plot_AmR:
        fig.add_hline(AmR, line_dash='dash',line_color='black',
                    annotation_text='AmR: ' + str(AmR))
    else:
        print('')
    # Specify annotations 
    fig.update_annotations(font_size=18, font_color='black')
    # Show fig in plotly
    st.plotly_chart(fig)
    st.caption('The mR-chart starts its life as a derived time series of moving range values.')

    st.markdown("### Building the PBC")

    st.markdown(
        """
        To transform the above time series into an XmR-chart, i.e. a Process Behavior Chart (PBC), the next step is to add process limits. Process limits are the defining features of PBCs. 
        Adding these limits facilitates discrimination between variation that is routine (common) and variation that is out-of-the-ordinary (special). For the XmR-chart, the UPL, LPL, and 
        URL are shown as red dotted lines. The mean and average moving range are shown as black dotted lines. 
        With the addition of these limits the **XmR-chart (PBC)** is complete! All that is left now is to interpret the results!
        """
    )
    
    st.markdown(" ### X-chart")
    # Create columns for controls
    colx, coly, colz = st.columns(3)
    with colx:
        plot_mean2 = st.checkbox('Show Mean ',value=True)
    with coly:
        plot_UPL = st.checkbox('Show UPL',value=True)
    with colz:
        plot_LPL = st.checkbox('Show LPL',value=True)

    # Create x-chart
    # Specify variables
    data = mR_df['Value']
    xlabels = mR_df.index.tolist()
    # Calculate basic statistics
    mean = round(data.mean(),1)
    AmR = round(mR_df['Moving range'].mean(),1)
    # Calculate process limits
    UPL = round(mean + (2.66*AmR),1)
    LPL = round(mean - (2.66*AmR),1)
    # Create figure object and plot data
    #fig = px.line(df, x=xlabels, y=parameter,markers=True)
    fig = px.line(df, x=xlabels, y=data,markers=True,
                labels={
                    'x':'Observation',
                    'y':'Value'
                })
    # Conditionally plot mean 
    if plot_mean2:
        fig.add_hline(mean, line_dash='dash',line_color='black',
                    annotation_text='Mean: ' + str(mean))
    if plot_UPL:
        fig.add_hline(UPL, line_dash='dash',line_color='red',
                    annotation_text='UPL: ' + str(UPL))
    if plot_LPL:
        fig.add_hline(LPL, line_dash='dash',line_color='red',
                    annotation_text='LPL: ' + str(LPL))
    # Add centerline
    #fig.add_hline(mean, line_dash='dash',line_color='black',
    #              annotation_text='Mean: ' + str(mean))
    # Specify annotations 
    fig.update_annotations(font_size=18, font_color='black')
    # Show fig in plotly
    st.plotly_chart(fig,use_container_width=True)
    st.caption('With the addition of the UPL and LPL the X-chart is complete.')

    
    st.markdown(" ### mR-chart")
    # Create columns for controls
    
    colx, coly = st.columns(2)
    with colx:
        plot_AmR2 = st.checkbox('Show Average Moving Range (AmR) ',value=True)
    with coly:
        plot_URL = st.checkbox('Show URL',value=True)
    
    # Specify variables for mR-plot
    data = mR_df['Moving range']
    xlabels = df.index.tolist()
    # Calculate basic statistics
    AmR = round(data.mean(),2) # In this case calculate average moving range
    URL = round(3.27*AmR,2)
    # Create figure object and plot moving range values
    #fig = px.line(df, x=xlabels, y=parameter,markers=True)
    fig = px.line(df,x=xlabels,y=data,markers=True,
                labels={
                    'x':'Observation',
                    'y':'Moving Range'
                })
    # Conditionally plot average moving range 
    if plot_AmR2:
        fig.add_hline(AmR, line_dash='dash',line_color='black',
                    annotation_text='AmR: ' + str(AmR))
    if plot_URL:
        fig.add_hline(URL, line_dash='dash',line_color='red',
                    annotation_text='URL: ' + str(URL))

    # Specify annotations 
    fig.update_annotations(font_size=18, font_color='black')
    # Show fig in plotly
    st.plotly_chart(fig)
    st.caption('With the addition of the URL what was previously a derived time series is now an mR-chart.')

    # check your work expander 
    st.markdown(" ## Check your work")
    with st.expander("Show complete dataframe"):
        st.dataframe(complete_df)
    
elif select_step == 'Interpreting the PBC':
    st.markdown("## Interpreting the PBC")

    st.markdown(
        """
        As you have come to see, Process Behavior Charts (PBCs) are built in six steps. These steps are:
        """
    )

    st.markdown(
        """
        1. Gather the data
        2. Calculate the mean
        3. Calculate the moving range
        4. Calculate the average moving range
        5. Calculate the process limits
        6. Put it all together!
        """
    )

    st.markdown(
        """
        While building a PBC is a quintessential first step toward improving processes and systems it is only a first step. 
        To take the insights of PBCs and turn them into actions requires the knowledge and knowhow of interpreting the results. 
        While we will not explore the full breadth and depth of this exploration here, what follows is acts as an introduction
        to the effort. 
        """
    )
    
    interpret_image_1 = Image.open(r'images\Interpreting PBC Flow Chart - Resource.png')
    
    st.image(interpret_image_1, caption="Interpreting a PBC revolves around answering a single question: \
             is all the data in the process limits? Whether it does or it doesn't use this flow chart to guide your efforts.")
         
    # interpret_image_2 = Image.open('Interpreting PBC Flow Chart.png')
    
# =============================================================================
#     with open("images\Interpreting PBC Flow Chart.png", "rb") as file:
# =============================================================================
    with open("Interpreting PBC Flow Chart.png", "rb") as file:
        
        btn = st.download_button(
            label='Download flowchart',
            data=file,
            file_name='Interpreting PBC flow chart.png',
            mime='image/png')

    st.markdown("### Start with characterization")

    st.markdown(
        """
        Interpreting a PBC starts with characterization. Characterization is the process of determining if future behavior of a process can be predicted
        (within the process limits). If it can, the process is characterized as predictable. If it cannot, the process is characterized as unpredictable. 
        Whether a process is characterized as predictable or unpredictable depends on the data's relationship with the process limits.
        """
    )
    
    st.markdown(
        """
        A process is said to be predictable when all of the values in the dataset fall within the process limits on the X-chart or are less than the upper
        range limit on the mR-chart. Conversely, a process is said to be unpredictable if one or more values falls outside the process limits on the X-chart
        or any value is greater than the URL on the mR-chart. 
        """)
    
    st.markdown("### Something to consider")
    
    st.markdown(
        """
        Worth noting is that characterization of unpredictable does not require values outisde process limits on both the X-chart and the mR-chart. From the
        perspective of characterization, the plots are inclusive. This means that when the X-chart (individual values plot) characterizes a process as unpredictable, the process is 
        unpredictable regardless of what the moving range plot shows. Similarly, if the mR-chart (moving range plot) characterizes the process as unpredictable but the X-chart 
        does not, the process is still unpredictable regardless of the X-chart. 
        """)
    
    st.markdown("### Your turn")
    
    xchart_Q1 = st.selectbox('Given the criteria for characterization, what is the characterization of the manufacturing process based on the X-chart below?',
                                ('-',
                                'Predictable',
                                'Unpredictable'))
    if xchart_Q1 == 'Predictable':
        st.markdown(":red[This process is not predictable. Think about the criteria that must be fullfilled for a process to be predictable and try again.]")
    elif xchart_Q1 == 'Unpredictable':
        st.markdown(":green[Correct! A process is characterized as unprdictable when one or more values fall outside the upper range limit (URL). Great work!] 😄")
        
    # Create columns for controls
    colx, coly, colz = st.columns(3)
    with colx:
        plot_mean2 = st.checkbox('Show Mean ',value=True)
    with coly:
        plot_UPL = st.checkbox('Show UPL',value=False)
    with colz:
        plot_LPL = st.checkbox('Show LPL',value=False)

    # Create x-chart
    # Specify variables
    data = mR_df['Value']
    xlabels = mR_df.index.tolist()
    # Calculate basic statistics
    mean = round(data.mean(),1)
    AmR = round(mR_df['Moving range'].mean(),1)
    # Calculate process limits
    UPL = round(mean + (2.66*AmR),1)
    LPL = round(mean - (2.66*AmR),1)
    # Create figure object and plot data
    #fig = px.line(df, x=xlabels, y=parameter,markers=True)
    fig = px.line(df, x=xlabels, y=data,markers=True,
                labels={
                    'x':'Observation',
                    'y':'Value'
                })
    # Conditionally plot mean 
    if plot_mean2:
        fig.add_hline(mean, line_dash='dash',line_color='black',
                    annotation_text='Mean: ' + str(mean))
    if plot_UPL:
        fig.add_hline(UPL, line_dash='dash',line_color='red',
                    annotation_text='UPL: ' + str(UPL))
    if plot_LPL:
        fig.add_hline(LPL, line_dash='dash',line_color='red',
                    annotation_text='LPL: ' + str(LPL))
    
    # Specify annotations 
    fig.update_annotations(font_size=18, font_color='black')
    # Show fig in plotly
    st.plotly_chart(fig,use_container_width=True)
    st.caption('A process is characterized a predictable when all values fall within the process limits. Given this criteria, how is this process characterized?')

    mRChart_Q1 = st.selectbox('Given the criteria for characterization, what is the characterization of the manufacturing process based on the mR-chart below?',
                                ('-',
                                'Predictable',
                                'Unpredictable'))
    if mRChart_Q1 == 'Predictable':
        st.markdown(":red[That's not correct. What criteria must be fullfilled for a process to be predictable?]")
    elif mRChart_Q1 == 'Unpredictable':
        st.markdown(":green[Correct! A process is characterized as unprdictable when one or more values fall outside the process limits. Great work!] 😄")

    colx, coly = st.columns(2)
    with colx:
        plot_AmR2 = st.checkbox('Show Average Moving Range (AmR) ',value=True)
    with coly:
        plot_URL = st.checkbox('Show URL',value=False)
    
    # Specify variables for mR-plot
    data = mR_df['Moving range']
    xlabels = df.index.tolist()
    # Calculate basic statistics
    AmR = round(data.mean(),2) # In this case calculate average moving range
    URL = round(3.27*AmR,2)
    # Create figure object and plot moving range values
    #fig = px.line(df, x=xlabels, y=parameter,markers=True)
    fig = px.line(df,x=xlabels,y=data,markers=True,
                labels={
                    'x':'Observation',
                    'y':'Moving Range'
                })
    # Conditionally plot average moving range 
    if plot_AmR2:
        fig.add_hline(AmR, line_dash='dash',line_color='black',
                    annotation_text='AmR: ' + str(AmR))
    if plot_URL:
        fig.add_hline(URL, line_dash='dash',line_color='red',
                    annotation_text='URL: ' + str(URL))

    # Specify annotations 
    fig.update_annotations(font_size=18, font_color='black')
    # Show fig in plotly
    st.plotly_chart(fig)
    st.caption('With the addition of the URL what was previously a derived time series is now an mR-chart.')

    st.markdown("### Next steps")
    
    st.markdown(
        """
        Given the characterization of unpredictable, we now know that both common and special causes of variation 
        are influcing the process. To move forward, to improve the process so that in the future it is characterized
        as predictable, time, attention, and resources must work to understand and eliminate the special causes 
        at their source. One path forward for achieving this is the evaluation of values that fall outside the 
        process limits.
        """)

    st.dataframe(special_cause_df)

    url = "https://static1.squarespace.com/static/5b722db6f2e6b1ad5053391b/t/6412641ab8d87704ac358cfe/1678926874938/Interpretating+a+Process+Behavior+Chart+-+Jim+Lehner.pdf"

    st.markdown(
        """
        The above dataframe lists all instances in the manufacturing dataset where the value either exceeded the UPL 
        (observation 41) or was equal to the LPL. Over the course of the dataset this occured five times. 
        Next steps necessitate an investigation of these values in the search for understanding. What was different about
        the process when these values were collected? How do these values compare to values that fell within limits? 
        Asking these pointed questions and performing the requisite analysis to find the answers is a task that will 
        invariably elucidate insights. To learn more about this process [click here](%s).
        """ % url)
        
# =============================================================================
# elif select_step == 'The Why-What-How of PBCs':
#     st.markdown(" ## Why use Process Behavior Charts?")
# 
#     st.markdown(" ## What are Process Behavior Charts?")
# 
#     st.markdown(
#         """
#         Process Behavior Charts, PBCs, are a graphical analysis tool for predicting how a process will behave in the future based on how it has behaved in the past. 
#         Such knowledge, regardless of industry or application, is quintessential to the improvement, optimization, and management of processes 
#         and systems. Rather than rely on gut feelings and hunches, PBCs unambiguously evaluate and characterize the variation associated with 
#         a process. Through this characterization time, attention, and resources are directed to areas that need it most so quantifiable improvement can be achieved. 
#         """
#     )
#     st.markdown("How do Process Behavior Charts work?")
#     st.markdown(
#         """
#         PBCs work by discriminating between the two types of variation that can influence a system. On the one hand there are sources of variation that are to be expected 
#         (common) and on the other there are sources of variation that are out-of-the-ordinary (special). The ability to identify sources of variation that are out-of-the-ordinary 
#         from sources of variation that are to be expected is facilitated by the PBCs process limits. Process limits, as opposed to specification limits, are the voice of the process. 
#         They are the boundary between sources of variation that are to be expected and sources of variation that are out-of-the-ordinary. 
#         """
#     )
# =============================================================================

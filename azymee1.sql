-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 17, 2021 at 12:50 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `azymee1`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
CREATE TABLE IF NOT EXISTS `appointment` (
  `A_ID` int(11) NOT NULL AUTO_INCREMENT,
  `P_ID` int(11) NOT NULL,
  `D_ID` int(11) NOT NULL,
  `Timing` varchar(255) NOT NULL,
  `Day` varchar(255) NOT NULL,
  `Status` varchar(255) NOT NULL,
  PRIMARY KEY (`A_ID`),
  KEY `P_ID` (`P_ID`),
  KEY `D_ID` (`D_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`A_ID`, `P_ID`, `D_ID`, `Timing`, `Day`, `Status`) VALUES
(1, 1, 1, '2312', 'Monday', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `counterquestions`
--

DROP TABLE IF EXISTS `counterquestions`;
CREATE TABLE IF NOT EXISTS `counterquestions` (
  `Disease_ID` int(11) NOT NULL,
  `Question1` varchar(1000) NOT NULL,
  `Question2` varchar(1000) NOT NULL,
  `Question3` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `counterquestions`
--

INSERT INTO `counterquestions` (`Disease_ID`, `Question1`, `Question2`, `Question3`) VALUES
(1, 'Do you feel sudden sensation that you\'re spinning or that the inside of your head is spinning.?', 'Do you experience A loss of balance or unsteadiness?', 'Are you feeling nausea or vomiting?'),
(2, 'Are you having blackheads or whiteheads on your body ?\r\n', 'Do you have an oily skin?\r\n', 'Are you having painful lumps under the skin \r\n'),
(3, ' Are you having Swollen lymph glands, mainly on the neck?', 'Are you expereincing skin and bumps?\r\n', 'Do you have any blood transfusion recently?'),
(4, 'Are you experiencing excessive watering from your eyes?', 'Are you having continuous sneezing and shortness of breath?', 'Are you feeling continuous chills and shivering?'),
(5, 'Do you have family history of Arthritis?\r\n', 'Are you above Ideal BMI level?\r\n', 'Are you experiencing  joint pain and stiffness?\r\n'),
(6, ' Are you having Wheezing sound while breathing and chest tightness?', 'Is your blood pressure normal ?', 'Do you have a lot of coughing at night?'),
(7, 'Do you Smoke cigarettes?\r\n', ' Do you have a lot of strain your neck?\r\n', 'Are you experiencing muscle spasms?\r\n'),
(8, 'Have you administrated vaccine against chicken pox?', 'Do you have itchy blisters and bumps all over your body ?', 'Are you suffering from fever?\r\n'),
(9, 'Are you having dark colored urine?\r\n', 'Are you experiencing excessive itching?\r\n', 'Have you suffered from hepatitis earlier?'),
(10, 'Are you having cough or runny nose?\r\n', 'Are you  having sore throat?\r\n', 'Are you suffering from fever?'),
(11, 'Are you having vomiting (at least 3 times in 24 hours)?', 'Are you suffering from severe headaches or pain behind the eyes.\r\n', 'Do  you have mosquitoes in your house and area?'),
(12, 'Are you experiencing increased thirst and urination?\r\n', 'Are you feeling numbness or tingling in the feet or hands?\r\n', 'Your wounds or cuts heal quickly?\r\n'),
(13, 'Do you feel excessive pain during bowel movements?\r\n', 'Do you feel cracks or lumps around your anus?\r\n', 'Are you suffering from constipation?\r\n'),
(14, 'Are you on any kind of medication?\r\n', 'Are you experiencing any rashes or itching on your body?\r\n', 'Are you experiencing shortness of breath or any allergic reactions?\r\n'),
(15, 'Are you experiencing any  skin color change or dyschromatic patches on your body?\r\n', 'Is your BMI above normal level?\r\n', 'Do you have suppressed immune system ?\r\n'),
(16, 'Are you experiencing lack of energy of lethargy in your body?\r\n', 'Are you experiencing dirrohea?', 'Have you eaten any contaminated food?\r\n'),
(17, 'Have you eaten something very spicy?', 'Are you feeling pain on the middle of your chest?\r\n', 'Are you experiencing any stomach pain or aciditiy\r\n'),
(18, 'Please visit your nearby hospital immediately \r\n', '', ''),
(19, 'Do you have yellowish skin?\r\n', 'Have you been exposed to unhygienic conditions?\r\n', 'Do you have abdominal pain or dirrohea?\r\n'),
(20, 'Are you suffering from stress?\r\n', 'Do you experience vision changes or severe headache?\r\n', 'Do you hear buzzing in ears?\r\n'),
(21, 'Are you feeling enlarged thyroid glands?\r\n', 'Do you have any family history of hyperthyroidism?\r\n', 'Are you feeling fast heartbeat?\r\n'),
(22, 'You previously had thyroid injury?\r\n', 'Do you have poor ability to tolerate cold?\r\n', 'Are you feeling depression and anxiety?\r\n'),
(23, 'Are you yakking higher doses of certain antidiabetic medications?\r\n', 'Do you skip meals?\r\n', 'Do you have kidney problems?\r\n'),
(24, 'Do you have red sores or blisters on the face, especially around the nose and mouth?\r\n', ' Are your rupture sores developing into honey-colored crusts?\r\n', 'Are you experiencing mild itching?\r\n'),
(25, 'Are you having yellowish color of skin and eyes\r\n', 'Are you fasting for long periods?\r\n', 'Have you experienced severe weight loss?'),
(26, 'Do you have mosquitos in your area?\r\n', 'Are you experiencing  anemia or bloody stools?\r\n', 'Are you experiencing muscle pain?\r\n'),
(27, 'Are you experiencing severe disturbance in vision?\r\n', 'Have you been through any depressed situation?\r\n', 'Are you having severe pain in half part of your head ?\r\n'),
(28, 'Is you BMI above normal level?\r\n', 'Do you feel pain and stiffness of joints (hand, knees, hip)?\r\n', 'Do you feel swelling of muscle around joints?\r\n'),
(29, 'Please visit your nearby hospital immediately \r\n', '', ''),
(30, 'Are you experiencing weight gain and bloating?\r\n', 'Are you having blood in your stool?', 'Are you experiencing stomach pain and nausea?\r\n'),
(31, ' Are you having cough with mucus or phlegm?\r\n', 'Do you feeling chest pain while coughing?\r\n', 'Are you experiencing periodic fever?\r\n'),
(32, 'Do you have Itching, burning, and painful lesions which may be accompanied by soreness?\r\n', 'Do you have dry, cracked skin which may be accompanied by bleeding?', 'Do you have any family history of psoriasis?\r\n'),
(33, 'Do you have Persistent cough (which lasts for more than 2 weeks)?\r\n', 'Do you have fever for more than 2 weeks?\r\n', 'Do you cough with blood in sputum?\r\n'),
(34, 'Are you experiencing dry cough?\r\n', 'Are you suffering from diarrhea or constipation?\r\n', 'Have you been exposed to contaminated food  or water?\r\n'),
(35, 'Are you suffering from any medical conditions such as diabetes, multiple sclerosis or stroke\r\n', 'Are you married?\r\n', 'Do you feel frequent urge to urinate?\r\n'),
(36, 'Do you have dark purple or blue prominent veins?\r\n', 'Do you have a sedentary life style?\r\n', 'Do you stand at a stretch for long hours routinely?\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `disease`
--

DROP TABLE IF EXISTS `disease`;
CREATE TABLE IF NOT EXISTS `disease` (
  `Disease_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Disease_Name` varchar(255) NOT NULL,
  `Disease_ Description` varchar(1000) NOT NULL,
  `Precautions` varchar(1000) NOT NULL,
  PRIMARY KEY (`Disease_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `disease`
--

INSERT INTO `disease` (`Disease_ID`, `Disease_Name`, `Disease_ Description`, `Precautions`) VALUES
(1, '(vertigo) Paroymsal  Positional Vertigo\r\n', 'Benign paroxysmal positional vertigo (BPPV) is one of the most common causes of vertigo is  the sudden sensation that you\'re spinning or that the inside of your head is spinning. Benign paroxysmal positional vertigo causes brief episodes of mild to intense dizziness.\r\n', 'Avoid abrupt body movement, Lie down and relax'),
(2, 'Acne', 'Acne vulgaris is the formation of comedones, papules, pustules, nodules, and/or cysts as a result of obstruction and inflammation of pilosebaceous units (hair follicles and their accompanying sebaceous gland). Acne develops on the face and upper trunk. It most often affects adolescents.\r\n', 'Bath twice , Avoid spicy food and drink plenty of water\r\n'),
(3, 'AIDS', 'Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV). By damaging your immune system, HIV interferes with your body\'s ability to fight infection and disease.\r\n', 'Avoid open cuts, Avoid blood transfusion and consult doctor'),
(4, 'Allergy', 'An allergy is an immune system response to a foreign substance that\'s not typically harmful to your body.They can include certain foods, pollen, or pet dander. Your immune system\'s job is to keep you healthy by fighting harmful pathogens.\r\n', 'Apply calamine and use ice to suppress itching'),
(5, 'Arthritis', 'Arthritis is the swelling and tenderness of one or more of your joints. The main symptoms of arthritis are joint pain and stiffness, which typically worsen with age. The most common types of arthritis are osteoarthritis and rheumatoid arthritis.\r\n', 'Use hot and cold therapy, massage or try acupuncture'),
(6, 'Bronchial Asthma', 'Bronchial asthma is a medical condition which causes the airway path of the lungs to swell and narrow. Due to this swelling, the air path produces excess mucus making it hard to breathe, which results in coughing, short breath, and wheezing. The disease is chronic and interferes with daily working.\r\n', 'switch to loose clothing, Take deep breaths and get away from trigger'),
(7, 'Cervical spondylosis', 'Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck. As the disks dehydrate and shrink, signs of osteoarthritis develop, including bony projections along the edges of bones (bone spurs).\r\n', 'Use heating pad or cold pack,Take otc pain reliver and consult doctor'),
(8, 'Chicken pox', 'Chickenpox is a highly contagious disease caused by the varicella-zoster virus (VZV). It can cause an itchy, blister-like rash. The rash first appears on the chest, back, and face, and then spreads over the entire body, causing between 250 and 500 itchy blisters.\r\n', 'Use Neem in bathing ,consume neem leaves, Take vaccine and avoid public places'),
(9, 'Chronic cholestasis\r\n', 'Chronic cholestatic diseases, whether occurring in infancy, childhood or adulthood, are characterized by defective bile acid transport from the liver to the intestine, which is caused by primary damage to the biliary epithelium in most cases\r\n', 'Take cold bath, add anti itch medicine, consult doctor and eat healthy\r\n'),
(10, 'Common Cold\r\n', 'The common cold is a viral infection of your nose and throat (upper respiratory tract). It\'s usually harmless, although it might not feel that way. Many types of viruses can cause a common cold.\r\n', 'drink vitamin c rich drinks, take vapors, avoid cold food and keep fever in check\r\n'),
(11, 'Dengue\r\n', 'an acute infectious disease caused by a flavivirus (species Dengue virus of the genus Flavivirus), transmitted by aedes mosquitoes, and characterized by headache, severe joint pain, and a rash. â€” called also breakbone fever, dengue fever.\r\n', 'Drink papaya leaf juice, avoid fatty and spicy food, keep mosquitos away and keep hydrated\r\n'),
(12, 'Diabetes\r\n', 'Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Blood glucose is your main source of energy and comes from the food you eat. Insulin, a hormone made by the pancreas, helps glucose from food get into your cells to be used for energy.\r\n', 'have balanced diet, exercise, consult doctor and maintain follow up\r\n'),
(13, 'Dimorphic hemmorhoids(piles)\r\n', 'Hemorrhoids, also spelled haemorrhoids, are vascular structures in the anal canal. In their ... Other names, Haemorrhoids, piles, hemorrhoidal disease .\r\n', 'avoid fatty and spicy food, consume witch hazel, warm bath with epsom salt, and consume alovera juice\r\n'),
(14, 'Drug Reaction\r\n', 'An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug or result from the combination of two or more drugs.\r\n', 'stop itching, consult nearest hospital	and stop taking drug.\r\n'),
(15, 'Fungal infection\r\n', 'In humans, fungal infections occur when an invading fungus takes over an area of the body and is too much for the immune system to handle. Fungi can live in the air, soil, water, and plants. There are also some fungi that live naturally in the human body. Like many microbes, there are helpful fungi and harmful fungi.\r\n', 'bath twice, use Dettol or neem in bathing water, keep infected area dry and use clean cloths\r\n'),
(16, 'Gastroenteritis\r\n', 'Gastroenteritis is an inflammation of the digestive tract, particularly the stomach, and large and small intestines. Viral and bacterial gastroenteritis are intestinal infections associated with symptoms of diarrhea , abdominal cramps, nausea , and vomiting .\r\n', 'stop eating solid food for while and try taking small sips of water.\r\n'),
(17, 'GERD\r\n', 'Gastroesophageal reflux disease, or GERD, is a digestive disorder that affects the lower esophageal sphincter (LES), the ring of muscle between the esophagus and stomach. Many people, including pregnant women, suffer from heartburn or acid indigestion caused by GERD.\r\n', 'avoid fatty and spicy food, avoid lying down after eating and maintain healthy weight	exercises\r\n'),
(18, 'Heart attack\r\n', 'The death of heart muscle due to the loss of blood supply. The loss of blood supply is usually caused by a complete blockage of a coronary artery, one of the arteries that supplies blood to the heart muscle.\r\n', 'call ambulance, chew or swallow aspirin	and keep calm\r\n'),
(19, 'Hepatitis \r\n', 'Inflammation of the liver due to the hepatitis C virus (HCV), which is usually spread via blood transfusion (rare), hemodialysis, and needle sticks. The damage hepatitis C does to the liver can lead to cirrhosis and its complications as well as cancer.\r\n', 'Consult nearest hospital, wash hands through, avoid fatty and spicy food and take 	medication\r\n'),
(20, 'Hypertension\r\n', 'Hypertension (HTN or HT), also known as high blood pressure (HBP), is a long-term medical condition in which the blood pressure in the arteries is persistently elevated. High blood pressure typically does not cause symptoms.\r\n', 'meditation, salt baths,	reduce stress	and  get proper sleep\r\n'),
(21, 'Hyperthyroidism', 'Hyperthyroidism (overactive thyroid) occurs when your thyroid gland produces too much of the hormone thyroxine. Hyperthyroidism can accelerate your body\'s metabolism, causing unintentional weight loss and a rapid or irregular heartbeat.\r\n', 'eat healthy, massage, use lemon balm and take radioactive iodine treatment\r\n'),
(22, 'Hypoglycemia', ' Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal. Glucose is your body\'s main energy source. Hypoglycemia is often related to diabetes treatment. But other drugs and a variety of conditions can cause low blood sugar in people who don\'t have diabetes.\r\n', 'lie down on side, check in pulse, drink sugary drinks and consult doctor\r\n'),
(23, 'Hypothyroidism', 'Hypothyroidism, also called underactive thyroid or low thyroid, is a disorder of the endocrine system in which the thyroid gland does not produce enough thyroid hormone.\r\n', 'reduce stress, exercise daily. eat healthy and get proper sleep\r\n'),
(24, 'Impetigo', 'Impetigo (im-puh-TIE-go) is a common and highly contagious skin infection that mainly affects infants and children. Impetigo usually appears as red sores on the face, especially around a child\'s nose and mouth, and on hands and feet. The sores burst and develop honey-colored crusts.\r\n', 'soak affected area in warm water, use antibiotics, remove scabs with wet compressed cloth and consult doctor\r\n'),
(25, 'Jaundice', 'Yellow staining of the skin and sclerae (the whites of the eyes) by abnormally high blood levels of the bile pigment bilirubin. The yellowing extends to other tissues and body fluids. Jaundice was once called the \"morbus regius\" (the regal disease) in the belief that only the touch of a king could cure it\r\n', 'drink plenty of water, consume milk thistle, eat fruits and high fiberous food.Take proper medication\r\n'),
(26, 'Malaria', 'An infectious disease caused by protozoan parasites from the Plasmodium family that can be transmitted by the bite of the Anopheles mosquito or by a contaminated needle or transfusion. Falciparum malaria is the most deadly type.\r\n', 'Consult nearest hospital, avoid oily food, avoid non veg food and keep mosquitos out\r\n'),
(27, 'Migraine', 'A migraine can cause severe throbbing pain or a pulsing sensation, usually on one side of the head. It\'s often accompanied by nausea, vomiting, and extreme sensitivity to light and sound. Migraine attacks can last for hours to days, and the pain can be so severe that it interferes with your daily activities.\r\n', 'meditation, reduce stress, use polaroid glasses in sun and	consult doctor\r\n'),
(28, 'Osteoarthristis', 'Osteoarthritis is the most common form of arthritis, affecting millions of people worldwide. It occurs when the protective cartilage that cushions the ends of your bones wears down over time.\r\n', 'acetaminophen, consult nearest hospital, salt baths and take proper medication\r\n'),
(29, 'Paralysis (brain hemorrhage)', 'Intracerebral hemorrhage (ICH) is when blood suddenly bursts into brain tissue, causing damage to your brain. Symptoms usually appear suddenly during ICH. They include headache, weakness, confusion, and paralysis, particularly on one side of your body.\r\n', 'Take proper massage, Eat healthy food, exercise daily and consult doctor\r\n'),
(30, 'Peptic ulcer diseae', 'Peptic ulcer disease (PUD) is a break in the inner lining of the stomach, the first part of the small intestine, or sometimes the lower esophagus. An ulcer in the stomach is called a gastric ulcer, while one in the first part of the intestines is a duodenal ulcer.', 'Avoid fatty spicy, eliminate milk and limit alcohol\r\n'),
(31, 'Pneumonia', 'Pneumonia is an infection in one or both lungs. Bacteria, viruses, and fungi cause it. The infection causes inflammation in the air sacs in your lungs, which are called alveoli. The alveoli fill with fluid or pus, making it difficult to breathe.', 'consult doctor, Take proper medication, rest and follow up\r\n'),
(32, 'Psoriasis', 'Psoriasis is a common skin disorder that forms thick, red, bumpy patches covered with silvery scales. They can pop up anywhere, but most appear on the scalp, elbows, knees, and lower back. Psoriasis can\'t be passed from person to person. It does sometimes happen in members of the same family.\r\n', 'wash hands with warm soapy water, stop bleeding using pressure, consult doctor	 and take salt baths\r\n'),
(33, 'Tuberculosis', 'Tuberculosis (TB) is an infectious disease usually caused by Mycobacterium tuberculosis (MTB) bacteria. Tuberculosis generally affects the lungs, but can also affect other parts of the body. Most infections show no symptoms, in which case it is known as latent tuberculosis.\r\n', 'Keep your mouth covered, consult doctor, Take proper medication and rest properly\r\n'),
(34, 'Typhoid', 'An acute illness characterized by fever caused by infection with the bacterium Salmonella typhi. Typhoid fever has an insidious onset, with fever, headache, constipation, malaise, chills, and muscle pain. Diarrhea is uncommon, and vomiting is not usually severe.\r\n', 'Eat high calorie vegitables, antiboitic therapy	 and consult doctor	'),
(35, 'Urinary tract infection', 'Urinary tract infection: An infection of the kidney, ureter, bladder, or urethra. Abbreviated UTI. Not everyone with a UTI has symptoms, but common symptoms include a frequent urge to urinate and pain or burning when urinating.\r\n', 'Drink plenty of water, increase vitamin c intake, drink cranberry juice	 and take probiotics\r\n'),
(36, 'Varicose veins', 'A vein that has enlarged and twisted, often appearing as a bulging, blue blood vessel that is clearly visible through the skin. Varicose veins are most common in older adults, particularly women, and occur especially on the legs.\r\n', 'Lie down flat and raise the leg high, use ointments, use vein compression and  don\'t stand still for long\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `D_ID` int(11) NOT NULL AUTO_INCREMENT,
  `D_Name` varchar(255) NOT NULL,
  `D_Email` varchar(255) NOT NULL,
  `D_Pass` varchar(255) NOT NULL,
  `D_Gender` varchar(255) NOT NULL,
  `D_Phone` varchar(255) NOT NULL,
  `D_Country` varchar(255) NOT NULL,
  `D_Timing` varchar(255) NOT NULL,
  `D_Day` varchar(255) NOT NULL,
  `Specialization` varchar(255) DEFAULT NULL,
  `Disease_ID` int(255) DEFAULT NULL,
  PRIMARY KEY (`D_ID`),
  KEY `Disease_ID` (`Disease_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`D_ID`, `D_Name`, `D_Email`, `D_Pass`, `D_Gender`, `D_Phone`, `D_Country`, `D_Timing`, `D_Day`, `Specialization`, `Disease_ID`) VALUES
(1, 'Maria', 'Mariahabib2207@Gmail.com', 'shmm7909?', 'Female', '03430481048', 'Pakistan', '1232', 'Monday', NULL, NULL),
(2, 'Masmin', 'A@gmail.com', 'shmm7909?', 'Gender', '343423423', 'Afganistan', '8-10 AM', 'Monday', NULL, NULL),
(3, 'dasdasd', 'b@gmail.com', 'asdfghjkl', 'Gender', '343243', 'Afganistan', '8-10 AM', 'Monday', NULL, NULL),
(4, 'masdasda', 'dasdas@gmail.com', 'aasdasd', 'Gender', '31233231', 'Afganistan', '8-10 AM', 'Monday', 'Audiologist', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS `patient` (
  `P_ID` int(11) NOT NULL AUTO_INCREMENT,
  `P_Name` varchar(255) NOT NULL,
  `P_Email` varchar(255) NOT NULL,
  `P_Password` varchar(255) NOT NULL,
  `P_Gender` varchar(30) NOT NULL,
  `P_Phone` varchar(11) NOT NULL,
  `P_Bloodgroup` varchar(30) NOT NULL,
  `P_DateOfBirth` varchar(255) NOT NULL,
  `P_Country` varchar(255) NOT NULL,
  `P_History` varchar(255) DEFAULT NULL,
  `A_ID` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`P_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`P_ID`, `P_Name`, `P_Email`, `P_Password`, `P_Gender`, `P_Phone`, `P_Bloodgroup`, `P_DateOfBirth`, `P_Country`, `P_History`, `A_ID`) VALUES
(1, 'Awais', 'adsa@gmail.com', 'shmm7909?', 'Gender', '312312312', 'A Positive', '2021-12-02', 'Afganistan', NULL, NULL),
(2, 'Usama', 'usama@gmail.com', 'sarkaar2207?', 'Male', '121313312', 'A+Ve', '22-July-1998', 'Pakistan', 'Fungal Infection\r\n', '2'),
(5, 'Maria', 'mariahabib2207@gmail.com', 'shmm7909?', 'Female', '03209045947', 'B+Ve', '22-July-1998', 'Pakistan', 'Acne', '1');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `patient` (`P_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`D_ID`) REFERENCES `doctor` (`D_ID`);

--
-- Constraints for table `doctor`
--
ALTER TABLE `doctor`
  ADD CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`Disease_ID`) REFERENCES `disease` (`Disease_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

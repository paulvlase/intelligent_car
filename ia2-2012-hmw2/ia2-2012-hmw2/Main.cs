using System;
using System.Collections.Generic;
using System.IO;

namespace ia22012hmw2
{
	class MainClass
	{
		static List<String>[] stringAttributes;
		static List<Example> dataSet;
		static Int32 nInputs;
		static Int32 nOutputs;

		public static void Main (String[] args)
		{
			if (args.Length != 4) {
				Console.WriteLine ("Usage: ./ia2-2012-hmw2.exe dataSetFile.cvs firstHidenLayer secondHiddenLayer learningRate");
				return;
			}

			String dataSetFile = args[0];
			Config.firstHiddenLayer = Int16.Parse(args[1]);
			Config.secondHiddenLayer = Int16.Parse (args[2]);
			Config.LearningRate = Double.Parse (args[3]);

			dataSet = new List<Example> ();
			nInputs = 0;
			nOutputs = 0;

			ReadDataSet (dataSetFile);
			NormalizeDataSet ();

			ShuffleDataSet ();

			Int32 iter = 0;
			Double learningMae = 0.0;
			Double learningMre = 0.0;
			Double testingMae  = 0.0;
			Double testingMre  = 0.0;

			StreamWriter cerinta2 = new StreamWriter("cerinta2.dat", true);
			StreamWriter cerinta3 = new StreamWriter("cerinta3.dat", true);

			Int32 times = 50;

			for (int i = 0; i < times; i++) {
				BackpropagationNetwork backnet = new BackpropagationNetwork (dataSet, nInputs, nOutputs);
				backnet.Simulate ();

				iter += backnet.iter;

				learningMae += backnet.learningMae;
				learningMre += backnet.learningMre;

				testingMae += backnet.testingMae;
				testingMre += backnet.testingMre;
			}

			iter /= times;

			learningMae /= times;
			learningMre /= times;

			testingMae  /= times;
			testingMre  /= times;

			cerinta2.WriteLine ("{0} {1} {2} {3} {4}", Config.firstHiddenLayer, Config.secondHiddenLayer, testingMae, testingMre, iter);
			cerinta3.WriteLine ("{0} {1}", Config.LearningRate, iter);

			Console.WriteLine ("learningMae = {0}, learningMre = {1} testingMae = {1}, testingMre = {2}", learningMae, learningMre, testingMae, testingMre);

			cerinta2.Flush();
			cerinta3.Flush ();
		}

		static void InitConverter (String[] header)
		{
			stringAttributes = new List<String>[header.Length];
			for (int i = 0; i < header.Length; i++) {
				stringAttributes [i] = new List<String> ();
			}
		}

		static double ConvertStringValue (String stringValue, int i)
		{

			List<String> stringValues = stringAttributes [i];
			if (stringValues.Contains (stringValue)) {
				Int32 pos = stringValues.IndexOf (stringValue);
				Console.WriteLine ("Cel mai prost");
				return pos + 0.0;
			} else {
				Console.WriteLine ("Sunt prost");
				stringValues.Add (stringValue);
				return stringValues.Count + 0.0;
			}
		}

		static void ReadDataSet (String inputFile)
		{
			using (StreamReader rd = new StreamReader(inputFile)) {
				if (rd.EndOfStream) {
					return;
				}
				// Citesc prima linie.
				String[] header = rd.ReadLine ().Split (',');
				InitConverter (header);

				// Numarul de atribute.
				nInputs = header.Length - 1;
				nOutputs = 1;

				while (!rd.EndOfStream) {
					String[] values = (rd.ReadLine ().Split (','));

					Double[] inValues = new Double[nInputs];
					Double[] outValues = new Double[nOutputs];

					/* Fill input values. */
					Boolean bRet;
					int i;
					for (i = 0; i < nInputs; i++) {
						bRet = Double.TryParse (values [i], out inValues [i]);

						if (bRet == false) {
							inValues [i] = ConvertStringValue (values [i], i);
						}
					}

					/* Fill desired output values. */
					bRet = Double.TryParse (values [nInputs + 0], out outValues [0]);

					if (bRet == false) {
						outValues [0] = ConvertStringValue (values [i], nInputs + 0);
					}
					dataSet.Add (new Example (inValues, outValues));
				}
			}
		}

		static void NormalizeDataSet ()
		{
			NormalizeInValues ();
			NormalizeOutValues ();
		}

		static void NormalizeInValues ()
		{
			for (int i = 0; i < nInputs; i++) {
				Double maxValue = Double.MinValue;
				Double minValue = Double.MaxValue;

				foreach (Example example in dataSet) {
					if (example.InValues [i] > maxValue) {
						maxValue = example.InValues [i];
					}

					if (example.InValues [i] < minValue) {
						minValue = example.InValues [i];
					}
				}

				foreach (Example example in dataSet) {
					example.InValues [i] = (example.InValues [i] - minValue) / (maxValue - minValue);
				}
			}
		}

		static void NormalizeOutValues ()
		{
			for (int i = 0; i < nOutputs; i++) {
				Double maxValue = Double.MinValue;
				Double minValue = Double.MaxValue;

				foreach (Example example in dataSet) {
					if (example.OutValues [i] > maxValue) {
						maxValue = example.OutValues [i];
					}

					if (example.OutValues [i] < minValue) {
						minValue = example.OutValues [i];
					}
				}

				foreach (Example example in dataSet) {
					example.OutValues [i] = (example.OutValues [i] - minValue) / (maxValue - minValue);
				}
			}
		}

		static void ShuffleDataSet ()
		{
			Int32 n = dataSet.Count;
			Random random = new Random ();
			while (n > 1) {
				Int32 k = (random.Next (0, n) % n);
				n--;

				Example example = dataSet [k];
				dataSet [k] = dataSet [n];
				dataSet [n] = example;
			}
		}

		private void WriteOutput ()
		{
			Console.WriteLine ("Output");
		}
	}
}

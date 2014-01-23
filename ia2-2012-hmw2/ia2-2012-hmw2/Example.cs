using System;

namespace ia22012hmw2
{
    public class Example
    {
        public double[] inValues;
        public double[] outValues;

        public Example(Double[] inValues, Double[] outValues)
        {
			this.inValues = inValues;
			this.outValues = outValues;
        }

		public Double[] InValues {
			get {return inValues; }
		}

		public Double[] OutValues {
			get { return outValues; }
		}
    }
}


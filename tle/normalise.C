

void doit(string filename)
{
  cout << "Normalise the file : " << filename << endl;

  // Open the file
  string s = filename+"?filetype=raw";
  TFile * f = TFile::Open(s.c_str());

  // compute the size (in float)
  int n = f->GetSize()/4.0;
  float * buf = new float[n];
  Bool_t b = f->ReadBuffer((char*)buf,n*4);

  // Find the max value
  float max = 0.0;
  for(unsigned int i=0; i<n; i++) {
    if (buf[i]> max) max = buf[i];
  }

  // Divide by the max
  for(unsigned int i=0; i<n; i++) {
    buf[i] = buf[i]/max;
  }
  f->Close();

  // Write the file
  TFile * output = TFile::Open(s.c_str(), "RECREATE");
  output->WriteBuffer((char*)buf, n*4);
  output->Close();
}

int normalise() {
  doit("output/dose-tle-Dose.raw");
  //  doit("output/dose-setle-Dose.raw");
  doit("output/dose-Dose.raw");
  exit();
}

import unittest
import classify_process
import isolate_process

class TestIsolateAndClassifyMethods(unittest.TestCase):
	# CLASSIFY TESTS
    def test_classifyImage(self):
    	label = classify_process.classifyImage('static/images/examples/walrus-input-example.png')

    	self.assertEqual(label, 'walrus')

    def test_classifyImageTiny(self):
    	label = classify_process.classifyImage('static/images/examples/tiny.jpg')

    	self.assertEqual(label, 'dolphin')

    def test_classifyImageGiant(self):
    	label = classify_process.classifyImage('static/images/examples/giant.jpg')

    	self.assertEqual(label, 'killer+whale')

    def test_classifyImageInvalidPath(self):
    	label = classify_process.classifyImage('invalidPathThatDoesNotExist')

    	self.assertEqual(label, None)

    def test_classifyImageNonImageFile(self):
    	label = classify_process.classifyImage('static/images/examples/notAnImage.txt')

    	self.assertEqual(label, None)

    def test_classifyImageCorruptImageFile(self):
    	label = classify_process.classifyImage('static/images/examples/corrupt.jpg')

    	self.assertEqual(label, None)

    #ISOLATE TESTS
    def test_isolateImage(self):
    	success = isolate_process.isolateImage('static/images/examples/walrus-input-example.png',None,None)

    	self.assertTrue(success)

    def test_isolateImageTiny(self):
    	success = isolate_process.isolateImage('static/images/examples/tiny.jpg',None,None)

    	self.assertTrue(success)    

    def test_isolateImageGiant(self):
    	success = isolate_process.isolateImage('static/images/examples/giant.jpg',None,None)

    	self.assertTrue(success)

    def test_isolateImageInvalidPath(self):
    	success = isolate_process.isolateImage('invalidPathThatDoesNotExist',None,None)

    	self.assertFalse(success)

    def test_isolateImageNonImageFile(self):
    	success = isolate_process.isolateImage('static/images/examples/notAnImage.txt',None,None)

    	self.assertFalse(success)

    def test_isolateImageCorruptImageFile(self):
    	success = isolate_process.isolateImage('static/images/examples/corrupt.jpg',None,None)

    	self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
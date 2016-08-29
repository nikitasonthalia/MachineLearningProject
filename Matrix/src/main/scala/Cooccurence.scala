import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
object Cooccurrence {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("matrix")
    .setMaster("local[7]") 
     .set("spark.executor.memory", "4g")
     .set("spark.driver.memory","5g"));
    val textFile = sc.textFile("/Users/vikashkamdar/Desktop/MLprojectOutput/train_week{0}.csv")
    val counts = textFile.map(line => {
    val token = line.split(",");
     val key = token(4);
     //For depot matrix
    //val valueD = token(1) +"#"+ token(10);
    // For product matrix
    val valueP = token(5) +"#"+ token(10);
    (key,valueP)}).groupByKey;
    output.coalesce(1).saveAsObjectFile("/Users/vikashkamdar/Desktop/MLprojectOutput/week{0}Pobjectoutput")
    
    val valuefile =  sc.objectFile[(Char, Seq[(String)])]("/Users/vikashkamdar/Desktop/week{0}Pobjectoutput/part-00000");
    val output= valuefile.persist(StorageLevel.MEMORY_AND_DISK_SER).flatMap( {
      case (userid, values) =>
      {
        var productIds = values.map(value=>value.split("#")(0));
        var demand = values.map(value=>value.split("#")(1));
        productIds.combinations(2).map(
          pairs => {
             {(pairs.mkString("#"), 1)}
          })
    }}).reduceByKey(_ + _);

  output.coalesce(1).saveAsTextFile("/Users/vikashkamdar/Desktop/MLprojectOutput/week7ProductMatrix")
 
}
  }